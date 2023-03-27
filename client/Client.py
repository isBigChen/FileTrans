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
        # logger.debug(LOGIN_REQUEST + request_data.encode())
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

    # 请求文件列表
    def require_filelist(self):
        self.client_socket.send(CATALOG_REQUEST)
        response_data = self.client_socket.recv(1024)
        if response_data[:2] == CATALOG_RESPONSE:
            response_data = (response_data[2:]).decode()
            # logger.debug(response_data)
            return response_data

    # 请求下载文件
    def download_file(self, filename):
        self.client_socket.send(FILE_REQUEST+filename.encode())
        response_data1 = self.client_socket.recv(1024)
        file_size = 0
        if response_data1[:2] == FILE_METADATA:
            file_size = response_data1[2:].decode()
            file_size = int(file_size)
        else:
            return

        self.client_socket.send(FILE_METADATA_OK + filename.encode())
        # logger.debug(FILE_METADATA_OK + filename.encode())
        self.download_file_content(filename, file_size)

    # 接收文件内容
    def download_file_content(self, file_name, file_size):
        recv_size = 0
        file_tmp = b''
        while recv_size < file_size:
            file_chunk = self.client_socket.recv(1024)
            file_chunk = file_chunk[2:]
            file_tmp += file_chunk
            recv_size += len(file_chunk)
        file_name = os.path.basename(file_name)
        file_name = "./download/" + file_name
        with open(file_name, "wb") as fp:
            fp.write(file_tmp)
        fp.close()
        logger.debug("[*] download file:%s complete" % file_name)