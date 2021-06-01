"""
Module with logic for generating AES Keys
"""

import json
import os
import random
import string

from Crypto.Cipher import AES
from Crypto import Random
from src.utils.path import init_directory, init_config


class AesKeyGenerator:  # pylint: disable=too-few-public-methods
    """
    Logic for generating AES Keys
    """
    def __init__(self, algorithm):
        self.key = Random.new().read(AES.block_size)
        self.algorithm = algorithm
        self.config = init_config()
        self.directory = self._init_aes_key_directory()

    def _init_aes_key_directory(self) -> str:
        """
        Init directories to store AES key
        """
        main_dir = self.config.get("directory").get("main_dir")
        asym_dir = self.config.get("directory").get("sym_dir")
        return init_directory(os.path.join(os.getcwd(), main_dir, asym_dir))

    def save_session_key(self) -> str:
        """
        Save session parameters (cipher algorithm and key) in file with randomized name.

        :return: name of file
        """
        filename = os.path.join(
            self.directory,
            ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(20))
        )
        data = {
            "algorithm": str(self.algorithm),
            "key:": str(self.key)
        }
        with open(filename, "w") as file:
            json.dump(data, file)
        return filename
