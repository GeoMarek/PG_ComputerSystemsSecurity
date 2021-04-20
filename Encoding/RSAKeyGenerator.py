import json
import os

from Crypto.PublicKey import RSA
from Utils.Path import init_dir


class RsaKeyGenerator:
    def __init__(self, algorithm):
        self.private_key = RSA.generate(self._getKeyLengthFrom(algorithm))
        self.public_key = self.private_key.publickey()
        self.filename = "my_rsa_key"
        self.dirname = init_dir(os.path.join(os.getcwd(), "StoredData", "Asymmetric"))
        self.priv_dir = init_dir(os.path.join(self.dirname, "private"))
        self.public_dir = init_dir(os.path.join(self.dirname, "public"))

    def save_keys(self):
        with open(os.path.join(self.priv_dir, self.filename), "wb") as private_keyfile:
            private_keyfile.write(self.private_key.exportKey(format='DER'))
        with open(os.path.join(self.public_dir, f"{self.filename}.pub"), "wb") as public_keyfile:
            public_keyfile.write(self.public_key.exportKey(format='DER'))
        return self.dirname

    @staticmethod
    def _getKeyLengthFrom(algorithm_name):
        with open(os.path.join(os.getcwd(), "config.json")) as file:
            config = json.load(file)
            algorithms = config["algorithms"]["asymmetric"]
            for key, value in algorithms.items():
                if key == algorithm_name:
                    return value
        raise Exception("Not found such algorithm")
