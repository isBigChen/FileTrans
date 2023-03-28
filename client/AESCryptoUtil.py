from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESCryptoUtil:
    def aes_encrypt(self, plaintext, key):
        # 创建AES加密器
        cipher = AES.new(key, AES.MODE_ECB)
        # 对明文进行填充
        plaintext = pad(plaintext, AES.block_size)
        # 加密
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext

    def aes_decrypt(self, ciphertext, key):
        # 创建AES解密器
        cipher = AES.new(key, AES.MODE_ECB)
        # 解密
        plaintext = cipher.decrypt(ciphertext)
        # 对明文进行去填充
        plaintext = unpad(plaintext, AES.block_size)
        return plaintext

