import socket
import json
import pickle
from .utils import *
from omnitools import randi, jd_and_utf8e, utf8d
from easyrsa import *


__ALL__ = ["SC"]


class SC(object):
    def __init__(self, host: str = "127.199.71.10", port: int = 39291) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, int(port)))
        self.key = None
        hash, public_key = self.request("get_pkey")
        public_key = b64d(public_key)
        if EasyRSA(public_key=public_key).verify(public_key, b64d(hash)):
            key = randb((RSA.import_key(public_key).n.bit_length()//8)-42)
            self.request("set_key", b64e(EasyRSA(public_key=public_key).encrypt(key)))
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


