import os

from Crypto.PublicKey import RSA


class RsaKeyGenerator:
    keys = {
        "rsa1024": 1024,
        "rsa2048": 2048
    }

    def __init__(self, filename, algorithm):
        self.private_key = RSA.generate(self.keys[algorithm])
        self.public_key = self.private_key.publickey()

        self.directory_name = "RSA_keys"
        self.private_dir = os.path.join(self.directory_name, "private")
        self.public_dir = os.path.join(self.directory_name, "public")

        self.init_directories()
        self.save_keys()

    def save_keys(self):
        print(self.public_key)
        print(self.private_key)

    def init_directories(self):
        # TODO: get path from user
        if not os.path.exists(self.directory_name):
            os.makedirs(self.directory_name)
            os.makedirs(self.private_dir)
            os.makedirs(self.public_dir)
        else:
            if not os.path.exists(self.public_dir):
                os.makedirs(self.public_dir)
            if not os.path.exists(self.private_dir):
                os.makedirs(self.private_dir)
