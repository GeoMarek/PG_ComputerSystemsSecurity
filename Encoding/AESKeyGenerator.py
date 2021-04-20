from Crypto.Cipher import AES
from Crypto import Random
from Utils.Path import init_dir
import os


class AesKeyGenerator:
    def __init__(self, algorithm):
        self.key = Random.new().read(AES.block_size)
        self.path = init_dir(os.path.join(os.getcwd(), "StoredData", "Symmetric"))
        self.algorithm = algorithm
