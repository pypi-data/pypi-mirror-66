from setuptools import setup, find_packages

setup(
    name="burst-ex",
    version='0.0.2',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    scripts=['burst/bin/burstctl'],
    install_requires=['setproctitle', 'twisted', 'events', 'netkit', 'click', 'redis'],
    url="https://pypi.org/project/burst-ex",
    license="MIT",
    author="QFun",
    author_email="code@qfun.com",
    description="twisted with master, proxy and worker",
)
