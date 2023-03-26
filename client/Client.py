import os
import sys
import socket
import getopt
import threading
from Logger import logger
from ProtocolCode import *

class Client:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            response_data = self.client_socket.recv(1024)
            logger.debug(response_data.decode())
        except Exception as e:
            logger.debug(e)

    def __del__(self):
        try:
            self.client_socket.send(DISCONNECT)
            self.client_socket.close()
            logger.debug("[-] disconnect")
        except Exception as e:
            logger.debug(e)

    # 登录请求+接收回包
    def login_request(self, request_data):
        # logger.debug(request_data)
        self.client_socket.send(LOGIN_REQUEST + request_data.encode())
        response_data = self.client_socket.recv(1024)
        if response_data[:2] == LOGIN_RESPONSE:
            if response_data[2] == b'1'[0]:
                return True
            else:
                return False

    # 注册请求+接收回包
    def regist_request(self, request_data):
        self.client_socket.send(REGISTER_REQUEST + request_data.encode())
        response_data = self.client_socket.recv(1024)
        if response_data[:2] == REGISTER_RESPONSE:
            if response_data[2] == b'1'[0]:
                return True
            else:
                return False

