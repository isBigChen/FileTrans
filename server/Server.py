from socketserver import BaseRequestHandler, ThreadingTCPServer
from Logger import logger
from ProtocolCode import *
from MysqlHandler import MysqlHandler
import json
import hashlib

SERVER_IP = "0.0.0.0"
SERVER_PORT = 6666


class Server(BaseRequestHandler):
    # overwrite handle() function
    def handle(self):
        self.client_ip, self.client_port = self.client_address
        logger.debug("[+] accept connect from %s:%s" % (self.client_ip, self.client_port))
        self.request.send("[+] connect success".encode())
        while True:
            request_data = self.request.recv(1024)
            if request_data[:2] == DISCONNECT:
                # 客户端关闭
                self.close_connect()
                return
            elif request_data[:2] == LOGIN_REQUEST:
                # 客户端登录
                self.check_login(request_data[2:])
            elif request_data[:2] == REGISTER_REQUEST:
                # 客户端注册
                self.check_regist(request_data[2:])



    # 客户端关闭
    def close_connect(self):
        logger.debug("[-] disconnect from %s:%s" % (self.client_ip, self.client_port))
        self.request.close()

    # 客户端注册
    def check_regist(self, request_data):
        request_data = request_data.decode()
        request_data = json.loads(request_data)
        username = request_data['username']
        password = request_data['password']
        # print(username, password)
        password = hashlib.sha1((username + password).encode("utf-8")).hexdigest()
        res = mysql_handler.operate_handler(
            "insert into users(username, password) values('%s', '%s')" % (username, password))
        self.request.send(REGISTER_RESPONSE + b'1')

    # 客户端登录
    def check_login(self, request_data):
        # logger.debug(request_data.decode())
        request_data = request_data.decode()
        request_data = json.loads(request_data)
        username = request_data['username']
        password = request_data['password']
        # print(username, password)
        password = hashlib.sha1((username+password).encode("utf-8")).hexdigest()

        res = mysql_handler.query_handler("select * from users where username='%s' and password='%s'" % (username, password))
        # print(res)
        if len(res) == 1:
            self.request.send(LOGIN_RESPONSE + b'1')
        else:
            self.request.send(LOGIN_RESPONSE + b'0')


if __name__ == "__main__":
    mysql_handler = MysqlHandler()
    server = ThreadingTCPServer((SERVER_IP, SERVER_PORT), Server)
    logger.debug("[+] Listening on %s", SERVER_PORT)
    server.serve_forever()