from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

key = b'b8mf\xd5\xa8Nr5\xb9\x05,\x98\xf8\\/'

def aes_encrypt(plaintext, key):
    # 创建AES加密器
    cipher = AES.new(key, AES.MODE_ECB)
    # 对明文进行填充
    plaintext = pad(plaintext, AES.block_size)
    # 加密
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def aes_decrypt(ciphertext, key):
    # 创建AES解密器
    cipher = AES.new(key, AES.MODE_ECB)
    # 解密
    plaintext = cipher.decrypt(ciphertext)
    # 对明文进行去填充
    plaintext = unpad(plaintext, AES.block_size)
    return plaintext

if __name__ == "__main__":
    text = b"['./AESCryptoutil.py', './_.py', './ProtocolCode.py', './requi"
    res1 = aes_encrypt(text, key)
    print(res1)
    res2 = aes_decrypt(res1, key)
    print(res2)