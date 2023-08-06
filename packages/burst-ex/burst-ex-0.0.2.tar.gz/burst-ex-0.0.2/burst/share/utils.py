# -*- coding: utf-8 -*-

import functools
import random

from .six import string_types
from .log import logger


def safe_call(func, *args, **kwargs):
    """
    安全调用
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error('exc occur. e: %s, func: %s', e, func, exc_info=True)
        # 调用方可以通过 isinstance(e, BaseException) 来判断是否发生了异常
        return e


def safe_func(func):
    """
    把函数变为安全的
    """
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        return safe_call(func, *args, **kwargs)
    return func_wrapper


def ip_bin_to_str(ip_num):
    """
    转换ip格式，从bin转为str
    :param ip_num:
    :return:
    """
    import socket
    return socket.inet_ntoa(ip_num)


def ip_str_to_bin(ip_str):
    """
    转化ip格式，从str转为bin
    :param ip_str:
    :return:
    """
    import socket
    return socket.inet_aton(ip_str)


def import_module_or_string(src):
    """
    按照模块导入或者字符串导入
    :param src:
    :return:
    """
    from .config import import_string
    return import_string(src) if isinstance(src, string_types) else src


class SequenceNumber(int):
    REQ_MAX = 0x7fffffff
    GRP_MAX = 0x3ff
    SND_MAX = 0x1f
    
    def __init__(self, x):
        super(SequenceNumber, self).__init__(x)
        self.request_index = x & self.REQ_MAX         # 0 - 2147483647
        self.sender_index = (x >> 52) & self.SND_MAX  # 0 - 31
        self.src_group_id = (x >> 42) & self.GRP_MAX  # 0 - 1023
        self.dst_group_id = (x >> 32) & self.GRP_MAX  # 0 - 1023
        
        self.connection_identifier = "%02d-%04d-%04d" % (self.sender_index, self.src_group_id, self.dst_group_id)
    
    def __str__(self):
        return "%s-%010d" % (self.connection_identifier, self.request_index)


class InnerCmdACK(object):
    SEND_RETRY = 20
    RECV_RETRY = 30
    
    @staticmethod
    def get_pubsub_channel(connection_identifier):
        return "inner_cmd_pubsub:%s" % connection_identifier
    
    @staticmethod
    def get_send_queue(connection_identifier):
        return "inner_cmd_send_queue:%s" % connection_identifier
    
    @staticmethod
    def get_recv_queue(connection_identifier):
        return "inner_cmd_recv_queue:%s" % connection_identifier


def hit(percent):
    return random.randint(1, 100) <= percent
