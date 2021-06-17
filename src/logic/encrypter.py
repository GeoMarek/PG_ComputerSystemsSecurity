import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

import ast


def get_file_name(file_path):
    return os.path.basename(file_path)


class Encrypter():

    def __init__(self, *args, **kwargs):
        pass

    def generate_session_key(self, size=32):
        key = get_random_bytes(size)
        return key

    def RSA_encrypt(self, msg, key):
        return key.encrypt(msg, 32)

    def RSA_decrypt(self, msg, key):
        return key.decrypt(ast.literal_eval(str(msg)))

    def encrypt_msg(self, msg, mode, key):
        data = msg.encode()
        data = bytearray(data)
        if mode == 'CBC':
            # Create cipher object and encrypt the data
            cipher = AES.new(key, AES.MODE_CBC)  # Create a AES cipher object with the key using the mode CBC
            ciphered_data = cipher.encrypt(pad(data, AES.block_size))  # Pad the input data and then encrypt
        elif mode == 'CFB':
            cipher = AES.new(key, AES.MODE_CFB)  # CFB mode
            ciphered_data = cipher.encrypt(data)  # Only need to encrypt the data, no padding required for this mode
        elif mode == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
            ciphered_data = cipher.encrypt(pad(data, AES.block_size))
        elif mode == 'OFB':
            cipher = AES.new(key, AES.MODE_OFB)
            ciphered_data = cipher.encrypt(data)
        if mode != 'ECB':
            ciphered_data = cipher.iv + ciphered_data
        return ciphered_data

    def decrypt_msg(self, msg, mode, key, iv_length=16):
        if mode != 'ECB':
            iv = msg[:iv_length]
            ciphered_data = msg[iv_length:]
        else:
            ciphered_data = msg

        if mode == 'CBC':
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
            original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size)  # Decrypt and then up-pad the result
        elif mode == 'CFB':
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
            original_data = cipher.decrypt(ciphered_data)  # No need to un-pad
        elif mode == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
            original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size)
        elif mode == 'OFB':
            cipher = AES.new(key, AES.MODE_OFB, iv=iv)
            original_data = cipher.decrypt(ciphered_data)

        return original_data.decode("utf-8")

    def encrypt_fun(self, file_path, mode, key):
        with open(file_path, 'rb') as input_file:
            input_data = input_file.read()

        enc_name = f"enc_{get_file_name(file_path)}"

        if mode == 'CBC':
            # Create cipher object and encrypt the data
            cipher = AES.new(key, AES.MODE_CBC)  # Create a AES cipher object with the key using the mode CBC
            ciphered_data = cipher.encrypt(pad(input_data, AES.block_size))  # Pad the input data and then encrypt
        elif mode == 'CFB':
            cipher = AES.new(key, AES.MODE_CFB)  # CFB mode
            ciphered_data = cipher.encrypt(input_data)  # Only need to encrypt the data, no padding required for this mode
        elif mode == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
            ciphered_data = cipher.encrypt(pad(input_data, AES.block_size))
        elif mode == 'OFB':
            cipher = AES.new(key, AES.MODE_OFB)
            ciphered_data = cipher.encrypt(input_data)

        # jezeli nie ma odpowiedniego folderu to go stworz
        if not os.path.exists('enc_files'):
            os.makedirs('enc_files')

        with open("enc_files/" + enc_name + ".enc", "wb") as enc_file:
            if mode != 'ECB':
                enc_file.write(cipher.iv)
            enc_file.write(ciphered_data)
        return "enc_files/" + enc_name + ".enc"

    def decrypt_fun(self, file_path, mode, key, iv_length=16):
        with open(file_path, "rb") as enc_file:
            if mode != 'ECB':
                iv = enc_file.read(iv_length)
            ciphered_data = enc_file.read()

        if mode == 'CBC':
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
            original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size)  # Decrypt and then up-pad the result
        elif mode == 'CFB':
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
            original_data = cipher.decrypt(ciphered_data)  # No need to un-pad
        elif mode == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
            original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size)
        elif mode == 'OFB':
            cipher = AES.new(key, AES.MODE_OFB, iv=iv)
            original_data = cipher.decrypt(ciphered_data)

        if not os.path.exists('dec_files'):
            os.makedirs('dec_files')
        file_name = get_file_name(file_path)
        file_name = file_name[:len(file_name)-4]
        with open("dec_files/" + file_name, "wb") as dec_file:
            dec_file.write(original_data)
