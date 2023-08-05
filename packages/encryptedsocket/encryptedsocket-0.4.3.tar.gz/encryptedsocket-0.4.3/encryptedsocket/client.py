import socket
import json
import pickle
from .utils import *
from omnitools import randi, jd_and_utf8e, utf8d
from easyrsa import *


__ALL__ = ["SC"]


class SC(object):
    def __init__(self, host: str = "127.199.71.10", port: int = 39291,
                 bits: int = 1024, public_key: bytes = None) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, int(port)))
        self.key = None
        hash, ingredients = self.request("get_akey")
        if EasyRSA(public_key=public_key).verify(jd(ingredients), b64d(hash)):
            b = randi(bits)
            g = ingredients["g"]
            p = ingredients["p"]
            bkey = pow(g, b, p)
            self.request("set_bkey", bkey)
            self.key = str(pow(ingredients["akey"], b, p))
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


