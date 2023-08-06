# -*- coding: utf-8 -*-

from twisted.internet.protocol import Protocol, Factory, connectionDone
from twisted.internet import reactor

from ...share.utils import safe_call, ip_str_to_bin, SequenceNumber, InnerCmdACK, hit
from ...share.log import logger, logger_cmd
from ..task_container import TaskContainer
from ...share.task import Task
from ...share import constants
from netkit.box import Box


class ClientConnectionFactory(Factory):

    def __init__(self, proxy):
        self.proxy = proxy

    def buildProtocol(self, addr):
        return ClientConnection(self, addr)


class ClientConnection(Protocol):
    _read_buffer = None

    # 客户端IP的数字
    _client_ip_num = None

    # 过期timer
    _expire_timer = None

    def __init__(self, factory, address):
        # address: IPv4Address
        self.factory = factory
        self.address = address
        self._read_buffer = b''

    def connectionMade(self):
        self.transport.setTcpNoDelay(True)

        self.factory.proxy.stat_counter.clients += 1

        # 转换string为int
        self._client_ip_num = ip_str_to_bin(self.address.host)

        self._set_expire_callback()

    def connectionLost(self, reason=connectionDone):
        self._clear_expire_callback()

        self.factory.proxy.stat_counter.clients -= 1

    def dataReceived(self, data):
        """
        当数据接受到时
        :param data:
        :return:
        """
        self._read_buffer += data

        while self._read_buffer:
            # 因为box后面还是要用的
            box = self.factory.proxy.app.box_class()
            ret = box.unpack(self._read_buffer)
            if ret == 0:
                # 说明要继续收
                return
            elif ret > 0:
                # 收好了
                # 不能使用双下划线，会导致别的地方取的时候变为 _Gateway__raw_data，很奇怪
                box._raw_data = self._read_buffer[:ret]
                self._read_buffer = self._read_buffer[ret:]
                safe_call(self._on_read_complete, box)
                continue
            else:
                # 数据已经混乱了，全部丢弃
                logger.error('buffer invalid. proxy: %s, ret: %d, read_buffer: %r',
                             self.factory.proxy, ret, self._read_buffer)
                self._read_buffer = b''
                return

    def write(self, data):
        """
        响应
        :return:
        """
        if self.connected:
            # 要求连接存在，并且连接还处于连接中
            self.transport.write(data)
            self.factory.proxy.stat_counter.client_rsp += 1
            return True
        else:
            return False

    def _on_read_complete(self, box):
        """
        完整数据接收完成
        :param box: 解析之后的box
        :return:
        """
        self.factory.proxy.stat_counter.client_req += 1
        self._set_expire_callback()

        # 获取映射的group_id
        group_id = self.factory.proxy.app.config['GROUP_ROUTER'](box)
        if group_id not in self.factory.proxy.app.config['GROUP_CONFIG']:
            logger.error('invalid group_id. group_id: %s', group_id)
            return

        if box.inner:
            if self.factory.proxy.app.config['INNER_CMD_SENDER_INDEX'] is not None:
                try:
                    if not self.patch_inner_cmd(box,
                                                self.factory.proxy.app,
                                                self.factory.proxy.redis_instance,
                                                self.factory.proxy.inner_cmd_indexes
                                                ):
                        return
                except Exception as e:
                    # 真的异常了，报警出来
                    logger_cmd.fatal('patch_inner_cmd raise exception. e: %s', e, exc_info=True)
                    
        # 打包成内部通信的task
        task = Task(dict(
            cmd=constants.CMD_WORKER_TASK_ASSIGN,
            client_ip_num=self._client_ip_num,
            body=box._raw_data,
        ))

        task_container = TaskContainer(task, self)
        self.factory.proxy.task_dispatcher.add_task(group_id, task_container)
    
    @staticmethod
    def patch_inner_cmd(box, app, rds, indexes):
        """
        安全起见，只丢弃了确定重复的包
        """
        if box.userdata <= 0:
            inner_box = Box()
            inner_box.unpack(box.body)
            logger_cmd.info("%s, sender dose not require ACK, box.userdata=%s, box.cmd=%s, inner_box.cmd=%s",
                            app.name, box.userdata, box.cmd, inner_box.cmd)
            return True
        
        sn = SequenceNumber(box.userdata)
        send_queue = InnerCmdACK.get_send_queue(sn.connection_identifier)
        recv_queue = InnerCmdACK.get_recv_queue(sn.connection_identifier)
        pub_channel = InnerCmdACK.get_pubsub_channel(sn.connection_identifier)
        prev_index = indexes[sn.connection_identifier]
        logger_cmd.debug("%s, %s, %s, %s, %s, prev %s", app.name, send_queue, recv_queue, pub_channel, sn, prev_index)
    
        # 多次循环，但只应该出队成功一次！
        for _ in xrange(InnerCmdACK.RECV_RETRY):
            head = rds.rpoplpush(send_queue, recv_queue)
            if head is None:
                logger_cmd.fatal("%s, FATAL ERROR! rpoplpush got None, need check right now! %s", app.name, sn)
                continue
        
            if int(head) == sn:
                # 正确收包
                if sn.request_index == 0 and prev_index != -1:
                    # 对端重置，牺牲掉第一个0号包做重置，依赖发送端超时重试
                    indexes[sn.connection_identifier] = -1  # 引用修改
                    # 避免被误判为丢包
                    rds.lrem(recv_queue, 1, head)
                    logger_cmd.info("%s, RESET, sn: %s, prev_index: %s", app.name, sn, prev_index)
                    return False
                
                # ACK
                percent = app.config['INNER_ACK_DROP_PERCENT']
                if hit(percent):
                    # 概率命中，丢弃
                    logger_cmd.info("%s, DROP ACK, hit %s%%, sn: %s", app.name, percent, sn)
                else:
                    # 正常应答
                    rds.publish(pub_channel, head)
                rds.lrem(recv_queue, 1, head)
                
                # 立即退出！
                # 队列里若有丢包产生的残留，交给下一次会话来清理
                break
            else:
                # 丢包了: 必然是更早的
                # 新请求已经过来了，那就没必要做publish
                rds.lrem(recv_queue, 1, head)
                logger_cmd.fatal("%s, LOST CMD, previous sn: %s, current sn: %s", app.name, SequenceNumber(int(head)), sn)
                continue
        else:
            # RECV_RETRY > SEND_RETRY，不应该走到这里
            logger_cmd.fatal("%s, FATAL ERROR! many rpoplpush failed, need check right now! sn: %s", app.name, sn)
            return True
        
        if sn.request_index == prev_index:
            logger_cmd.info("%s, REPEAT, sn: %s", app.name, sn)
            return False
        else:
            if sn.request_index > prev_index:
                logger_cmd.debug("%s, VALID, sn: %s, prev_index: %s", app.name, sn, prev_index)
            else:
                # 对端重置，且0号包彻底失败了
                logger_cmd.fatal("%s, FATAL ERROR, sn: %s, prev_index: %s", app.name, sn, prev_index)
                
            indexes[sn.connection_identifier] = sn.request_index  # 引用修改
            return True
        
    def _set_expire_callback(self):
        """
        注册超时之后的回调
        :return:
        """

        if self.factory.proxy.app.config['PROXY_CLIENT_TIMEOUT'] is None:
            return

        self._clear_expire_callback()

        self._expire_timer = reactor.callLater(
            self.factory.proxy.app.config['PROXY_CLIENT_TIMEOUT'], self._expire_callback
        )

    def _clear_expire_callback(self):
        """
        清空超时之后的回调
        :return:
        """
        if self._expire_timer:
            self._expire_timer.cancel()
            self._expire_timer = None

    def _expire_callback(self):
        """
        能关闭的话，就关闭掉
        :return:
        """
        self._expire_timer = None

        if self.transport and self.transport.connected:
            self.transport.loseConnection()
