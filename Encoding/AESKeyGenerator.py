import json
import string
import random

from Crypto.Cipher import AES
from Crypto import Random
from Utils.Path import init_dir, init_config
import os


class AesKeyGenerator:
    def __init__(self, algorithm):
        self.key = Random.new().read(AES.block_size)
        self.algorithm = algorithm
        self.config = init_config()
        self.directory = self._initDirectory()

    def _initDirectory(self):
        main_dir = self.config.get("directory").get("main_dir")
        asym_dir = self.config.get("directory").get("sym_dir")
        return init_dir(os.path.join(os.getcwd(), main_dir, asym_dir))

    def save_session_key(self):
        filename = os.path.join(
            self.directory,
            ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(20))
        )
        # TODO: here add session parameters to store
        data = {
            "algorithm": str(self.algorithm),
            "key:": str(self.key)
        }
        with open(filename, "w") as file:
            json.dump(data, file)
        return filename
