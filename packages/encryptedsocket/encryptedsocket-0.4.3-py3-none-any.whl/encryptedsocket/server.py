import socket
import json
import pickle
import threading
from .utils import *
from omnitools import encryptedsocket_function, randi, p, utf8d
from debugging import *
from easyrsa import *


__ALL__ = ["SS"]


class SS(object):
    def __init__(self, functions: encryptedsocket_function = None, host: str = "127.199.71.10", port: int = 39291,
                 bits: int = 1024, private_key: bytes = None) -> None:
        self.sema = threading.Semaphore(1)
        self.terminate = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, int(port)))
        self.s.listen(5)
        self.__key = {}
        self.functions = functions or {}
        self.rsae = lambda v: EasyRSA(private_key=private_key).encrypt(v)
        self.sign = lambda v: EasyRSA(private_key=private_key).sign(v)
        self.__a = randi(bits)
        self.__g = randi(bits)
        self.__p = randi(bits)
        self.__akey = pow(self.__g, self.__a, self.__p)

    def handler(self, conn: socket.socket, addr: tuple) -> None:
        self.sema.acquire()
        uid = addr[0]+":"+str(addr[1])
        p(f"connected\t{uid}")
        try:
            while True:
                request = utf8d(conn.recv(1024*4))
                if not request:
                    self.__key.pop(uid)
                    break
                response = {}
                if uid in self.__key:
                    request = decrypt(self.__key[uid], request)
                else:
                    request = jl(request)
                if request["command"] == "get_akey":
                    v = dict(g=self.__g, p=self.__p, akey=self.__akey)
                    response = (
                        b64e(self.sign(jd(v))),
                        v
                    )
                elif request["command"] in self.functions:
                    try:
                        response = self.functions[request["command"]](request["data"])
                    except:
                        response = debug_info()
                try:
                    from omnitools import jd_and_utf8e
                    response = jd_and_utf8e(response)
                except TypeError:
                    response = pickle.dumps(response)
                if uid in self.__key:
                    response = encrypt(self.__key[uid], response)
                conn.sendall(response)
                if request["command"] == "set_bkey":
                    self.__key[uid] = str(pow(request["data"], self.__a, self.__p))
        except:
            p(debug_info()[0])
        finally:
            conn.close()
            self.sema.release()
            p(f"disconnected\t{uid}")

    def start(self) -> None:
        try:
            while not self.terminate:
                conn, addr = self.s.accept()
                threading.Thread(target=self.handler, args=(conn, addr)).start()
        except Exception as e:
            if not self.terminate:
                raise e

    def stop(self) -> bool:
        self.terminate = True
        self.s.close()
        return True


