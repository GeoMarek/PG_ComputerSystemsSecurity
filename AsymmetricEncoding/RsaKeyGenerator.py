import json
import os

from Crypto.PublicKey import RSA


class RsaKeyGenerator:
    keys = {
        "rsa1024": 1024,
        "rsa2048": 2048
    }

    def __init__(self, dirpath, filename, algorithm):
        self.private_key = RSA.generate(self._getKeyLengthFrom(algorithm))
        self.public_key = self.private_key.publickey()
        self.filename = filename
        self.directory_name = os.path.join(dirpath, filename)

    def save_keys(self):
        with open(os.path.join(self.directory_name, self.filename), "wb") as private_keyfile:
            private_keyfile.write(self.private_key.exportKey(format='DER'))
        with open(os.path.join(self.directory_name, f"{self.filename}.pub"), "wb") as public_keyfile:
            public_keyfile.write(self.public_key.exportKey(format='DER'))
        return self.directory_name

    def init_directories(self):
        if not os.path.exists(self.directory_name):
            os.makedirs(self.directory_name)

    @staticmethod
    def _getKeyLengthFrom(algorithm_name):
        with open(os.path.join(os.getcwd(), "config.json")) as file:
            config = json.load(file)
            algorithms = config["algorithms"]["asymmetric"]
            for key, value in algorithms.items():
                if key == algorithm_name:
                    return value
        raise Exception("Not found such algorithm")
