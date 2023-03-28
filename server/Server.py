from socketserver import BaseRequestHandler, ThreadingTCPServer
from Logger import logger
from ProtocolCode import *
from MysqlHandler import MysqlHandler
import json
import hashlib
import os
from pymysql.converters import escape_string
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from AESCryptoutil import AESCryptoUtil
import time


SERVER_IP = "0.0.0.0"
SERVER_PORT = 6666


class Server(BaseRequestHandler):
    # overwrite handle() function
    def handle(self):
        self.client_ip, self.client_port = self.client_address
        logger.debug("[+] accept connect from %s:%s" % (self.client_ip, self.client_port))
        # self.request.send("[+] connect success".encode())
        self.aes_util = AESCryptoUtil()
        # 会话密钥
        self.session_key = session_key = os.urandom(32)
        # 协商密钥
        self.server_secure_pannel_init()
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
            elif request_data[:2] == CATALOG_REQUEST:
                # 获取文件列表
                self.get_filelist()
            elif request_data[:2] == FILE_REQUEST:
                # 发送文件大小数据元
                self.request_file_size(request_data[2:])
            elif request_data[:2] == FILE_METADATA_OK:
                # 发送文件
                self.send_file_content(request_data[2:])

    def server_secure_pannel_init(self):
        try:
            # 使用客户端的公钥加密
            with open('./keys/client_public_key.pem', 'r') as fp:
                client_pub_key = RSA.import_key(fp.read())
            fp.close()
            client_pub_rsa = PKCS1_OAEP.new(client_pub_key)
            client_encrypted_session_key = client_pub_rsa.encrypt(self.session_key)
            # 服务端签名
            with open('./keys/server_private_key.pem', 'r') as fp:
                server_pri_key = RSA.import_key(fp.read())
            fp.close()
            session_key_hash = SHA256.new(self.session_key)
            signature = pkcs1_15.new(server_pri_key).sign(session_key_hash)
            self.request.send(client_encrypted_session_key + signature)
        except Exception as e:
            logger.debug(e)

    # 发送文件
    def send_file_content(self, filename):
        time.sleep(10)
        filename = self.aes_util.aes_decrypt(filename, self.session_key)
        filename = filename.decode()
        file_size = os.stat(filename).st_size

        with open(filename, "rb") as fp:
            data = fp.read(1024-5)
            while data:
                # logger.debug(FILE_CONTENT + data)
                data = self.aes_util.aes_encrypt(data, self.session_key)
                self.request.send(FILE_CONTENT + data)
                data = fp.read(1024-5)
        fp.close()
        logger.debug("[*] %s download file:%s" % (self.client_ip, filename))


    # 获取文件大小数据元
    def request_file_size(self, filename):
        filename = self.aes_util.aes_decrypt(filename, self.session_key)
        filename = filename.decode()
        file_size = os.stat(filename).st_size
        file_size = str(file_size)
        # logger.debug(FILE_METADATA + file_size.encode())
        file_size = self.aes_util.aes_encrypt(file_size.encode(), self.session_key)
        self.request.send(FILE_METADATA+file_size)


    # 获取文件列表
    def get_filelist(self):
        file_list = []
        for path, file_dir, files in os.walk('./'):
            for file_name in files:
                cur_file = os.path.join(path, file_name)
                file_list.append(cur_file)
        file_list = str(file_list).encode()
        file_list_response = self.aes_util.aes_encrypt(file_list, self.session_key)

        send_count = len(file_list_response)//(64-2) + 1
        for i in range(send_count):
            if i != send_count-1:
                file_list_response_chunk = file_list_response[i*(64-2):i*(64-2)+(64-2)]
                self.request.send(CATALOG_RESPONSE + file_list_response_chunk)
            else:
                file_list_response_chunk = file_list_response[i * (64 - 2):]
                self.request.send(CATALOG_RESPONSE + file_list_response_chunk)



    # 客户端关闭
    def close_connect(self):
        logger.debug("[-] disconnect from %s:%s" % (self.client_ip, self.client_port))
        self.request.close()

    # 客户端注册
    def check_regist(self, request_data):
        request_data = self.aes_util.aes_decrypt(request_data, self.session_key)
        request_data = request_data.decode()
        request_data = json.loads(request_data)
        username = request_data['username']
        password = request_data['password']
        username = escape_string(username)
        password = escape_string(password)
        # print(username, password)
        password = hashlib.sha1((username + password).encode("utf-8")).hexdigest()
        try:
            res = mysql_handler.operate_handler("insert into users(username, password) values('%s', '%s')" % (username, password))
            response_data = self.aes_util.aes_encrypt(b'1', self.session_key)
            response_data = REGISTER_RESPONSE + response_data
            self.request.send(response_data)
        except Exception as e:
            response_data = self.aes_util.aes_encrypt(b'0', self.session_key)
            response_data = REGISTER_RESPONSE + response_data
            self.request.send(response_data)

    # 客户端登录
    def check_login(self, request_data):
        request_data = self.aes_util.aes_decrypt(request_data, self.session_key)
        # logger.debug(request_data.decode())
        request_data = request_data.decode()
        request_data = json.loads(request_data)
        username = request_data['username']
        password = request_data['password']
        username = escape_string(username)
        password = escape_string(password)
        # print(username, password)
        password = hashlib.sha1((username+password).encode("utf-8")).hexdigest()

        query_str = "select * from users where username='%s' and password='%s'" % (username, password)
        # logger.debug(query_str)
        try:
            res = mysql_handler.query_handler(query_str)
            if len(res) >= 1:
                response_data = self.aes_util.aes_encrypt(b'1', self.session_key)
                response_data = LOGIN_RESPONSE + response_data
            else:
                response_data = self.aes_util.aes_encrypt(b'0', self.session_key)
                response_data = LOGIN_RESPONSE + response_data
            self.request.send(response_data)
        except Exception as e:
            response_data = self.aes_util.aes_encrypt(b'0', self.session_key)
            response_data = LOGIN_RESPONSE + response_data
            self.request.send(response_data)



if __name__ == "__main__":
    mysql_handler = MysqlHandler()
    server = ThreadingTCPServer((SERVER_IP, SERVER_PORT), Server)
    logger.debug("[+] Listening on %s", SERVER_PORT)
    server.serve_forever()