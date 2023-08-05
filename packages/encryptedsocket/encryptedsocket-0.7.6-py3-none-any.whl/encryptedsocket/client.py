import socket
import pickle
from .utils import *
from omnitools import jd_and_utf8e, utf8d, args
from easyrsa import *


__ALL__ = ["SC"]


class SC(object):
    def __init__(self, host: str = "127.199.71.10", port: int = 39291) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, int(port)))
        self.key = None
        hash, public_key = self.request("get_pkey")
        public_key = b64d(public_key)
        rsa = EasyRSA(public_key=public_key)
        if rsa.verify(public_key, b64d(hash)):
            key = randb(256)
            org_key = key
            _key = []
            max_msg_size = EasyRSA(public_key=public_key).max_msg_size()
            while org_key:
                _key.append(b64e(rsa.encrypt(org_key[:max_msg_size])))
                org_key = org_key[max_msg_size:]
            self.request("set_key", args(*_key))
            self.key = key
        else:
            raise Exception("current connection is under MITM attack")

    def request(self, command: str, data: Any = None) -> Any:
        request = dict(command=command, data=data)
        try:
            request = jd_and_utf8e(request)
        except:
            request = pickle.dumps(request)
        if self.key:
            request = encrypt(self.key, request)
        self.s.send(request)
        while True:
            response = utf8d(self.s.recv(1024*4))
            if response:
                if self.key:
                    return decrypt(self.key, response)
                else:
                    return jl(response)


