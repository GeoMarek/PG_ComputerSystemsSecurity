"""
Module with logic for generating RSA Keys
"""
import os

from Crypto.PublicKey import RSA
from src.logic.utils.path import init_directory, init_config


class RsaKeyGenerator:  # pylint: disable=too-few-public-methods
    """
    Logic for generating RSA Keys
    """
    def __init__(self, algorithm):
        self.config = init_config()
        self.private_key = RSA.generate(self._get_key_length_based_on(algorithm))
        self.public_key = self.private_key.publickey()
        self.filename = "my_rsa_key"
        self.dirname = self._init_directories()
        self.priv_dir = init_directory(os.path.join(self.dirname, "private"))
        self.public_dir = init_directory(os.path.join(self.dirname, "public"))

    def save_keys(self) -> str:
        """
        Generate and save keyfiles in specified directory. After this return this directory name.
        """
        with open(os.path.join(self.priv_dir, self.filename), "wb") as private_keyfile:
            private_keyfile.write(self.private_key.exportKey(format='DER'))
        with open(os.path.join(self.public_dir, f"{self.filename}.pub"), "wb") as public_keyfile:
            public_keyfile.write(self.public_key.exportKey(format='DER'))
        return self.dirname

    def _get_key_length_based_on(self, algorithm_name: str) -> int:
        """
        Get key length based on algorith name. If such algorithm doesnt exist raise an exception
        """
        algorithms = self.config.get("algorithms").get("asymmetric")
        for key, value in algorithms.items():
            if key == algorithm_name:
                return value
        raise Exception("Not found such algorithm")

    def _init_directories(self) -> str:
        """
        Init directory for storing RSA keys and return its name
        """
        main_dir = self.config.get("directory").get("main_dir")
        asym_dir = self.config.get("directory").get("asym_dir")
        return init_directory(os.path.join(os.getcwd(), main_dir, asym_dir))
