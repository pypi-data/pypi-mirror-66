"""
convenience functions for sharing objects with multiple processes or machines
"""

from multiprocessing.managers import BaseManager
from threading import Thread
import logging

log = logging.getLogger(__name__)

default_ip = "127.0.0.1"
default_port = 4006
default_authkey = b"aaa"


class Manager(BaseManager):
    pass


def create_server(obj, ip=None, port=None, authkey=None):
    """ share object so it can be accessed from multiple processes

    :param obj: object to publish on server
    :param ip: ip address for server
    :param port: port number for server
    :param authkey: binary key to be used by server and client. None is b"aaa"
    """

    def target(obj):
        Manager.register("get_obj", callable=lambda: obj)
        m = Manager(ip=ip, port=port, authkey=authkey)
        try:
            s = m.get_server()
            s.serve_forever()
        except OSError:
            log.warning("server already running")

    ip = ip or default_ip
    port = port or default_port
    authkey = authkey or default_authkey

    t = Thread(target=target, daemon=True, args=(obj,))
    t.start()


def create_client(ip=None, port=None, authkey=None):
    """ return proxy for object in another process

    :param ip: ip address for server
    :param port: port number for server
    :param authkey: binary key to be used by server and client. None is b"aaa"
    :return: proxy_object for use in processes
    """
    ip = ip or default_ip
    port = port or default_port
    authkey = authkey or default_authkey

    Manager.register("get_obj")
    m = Manager(ip=ip, port=port, authkey=authkey)
    m.connect()
    return m.get_obj()
