import os
import socket
import threading
from Logger import logger
from ProtocolCode import *
from AESCryptoUtil import AESCryptoUtil
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class Client:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port
        # 协商的密钥
        self.session_key = None
        self.aes_util = AESCryptoUtil()
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            # 协商密钥
            self.client_secure_pannel_init()
        except Exception as e:
            logger.debug(e)

    def __del__(self):
        try:
            self.client_socket.send(DISCONNECT)
            self.client_socket.close()
            logger.debug("[-] disconnect")
        except Exception as e:
            logger.debug(e)

    # 协商密钥
    def client_secure_pannel_init(self):
        response_data = self.client_socket.recv(1024)
        client_encrypted_session_key = response_data[:128]
        signature = response_data[128:]
        with open('./keys/client_private_key.pem', 'r') as fp:
            client_pri_key = RSA.import_key(fp.read())
        fp.close()
        # 客户端私钥解密
        client_pri_rsa = PKCS1_OAEP.new(client_pri_key)
        self.session_key = client_pri_rsa.decrypt(client_encrypted_session_key)
        # 使用服务端公钥验证签名
        with open('./keys/server_public_key.pem', 'r') as fp:
            server_pub_key = RSA.import_key(fp.read())
        fp.close()
        session_key_hash = SHA256.new(self.session_key)
        try:
            # 验证签名
            pkcs1_15.new(server_pub_key).verify(session_key_hash, signature)
            logger.debug("[+] connect success")
            # print(self.session_key)
        except Exception as e:
            # print(e)
            logger.debug(e)

    # 登录请求+接收回包
    def login_request(self, request_data):
        # 加密
        # logger.debug(request_data)
        request_data = request_data.encode()
        request_data = self.aes_util.aes_encrypt(request_data, self.session_key)
        self.client_socket.send(LOGIN_REQUEST + request_data)

        # 接收+解密
        response_data = self.client_socket.recv(1024)
        if response_data[:2] == LOGIN_RESPONSE:
            response_data = self.aes_util.aes_decrypt(response_data[2:], self.session_key)
            # print(response_data)
            if response_data == b'1':
                return True
            else:
                return False

    # 注册请求+接收回包
    def regist_request(self, request_data):
        # 加密
        request_data = request_data.encode()
        request_data = self.aes_util.aes_encrypt(request_data, self.session_key)
        self.client_socket.send(REGISTER_REQUEST + request_data)
        # 接收+解密
        response_data = self.client_socket.recv(1024)
        if response_data[:2] == REGISTER_RESPONSE:
            response_data = self.aes_util.aes_decrypt(response_data[2:], self.session_key)
            if response_data == b'1':
                return True
            else:
                return False

    # 请求文件列表
    def require_filelist(self):
        self.client_socket.send(CATALOG_REQUEST)
        file_list_byte = b''
        response_data = self.client_socket.recv(64)
        while True:
            if response_data[:2] == CATALOG_RESPONSE:
                response_data_content = (response_data[2:])
                file_list_byte += response_data_content
                # logger.debug(file_list_byte)
            if len(response_data) == 64:
                response_data = self.client_socket.recv(64)
            else:
                break
        file_list_byte = self.aes_util.aes_decrypt(file_list_byte, self.session_key)
        file_list = file_list_byte.decode()
        return file_list

    # 请求下载文件
    def download_file(self, filename):
        filename_str = filename
        filename = self.aes_util.aes_encrypt(filename.encode(), self.session_key)
        self.client_socket.send(FILE_REQUEST+filename)
        response_data1 = self.client_socket.recv(1024)
        if response_data1[:2] == FILE_METADATA:
            file_size = self.aes_util.aes_decrypt(response_data1[2:], self.session_key)
            file_size = file_size.decode()
            file_size = int(file_size)
        else:
            return

        self.client_socket.send(FILE_METADATA_OK + filename)
        # logger.debug(FILE_METADATA_OK + filename.encode())
        self.download_file_content(filename_str, file_size)

    # 接收文件内容
    def download_file_content(self, file_name, file_size):
        recv_size = 0
        file_tmp = b''
        while recv_size < file_size:
            file_chunk = self.client_socket.recv(1024)
            file_chunk = file_chunk[2:]
            file_chunk = self.aes_util.aes_decrypt(file_chunk, self.session_key)
            file_tmp += file_chunk
            recv_size += len(file_chunk)
        file_name = os.path.basename(file_name)
        file_name = "./download/" + file_name
        with open(file_name, "wb") as fp:
            fp.write(file_tmp)
        fp.close()
        logger.debug("[*] download file:%s complete" % file_name)