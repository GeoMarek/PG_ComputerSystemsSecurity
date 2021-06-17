"""
A collection of useful functions that work on paths
"""

import json
import os
from typing import Dict
from Crypto.PublicKey import RSA


def init_directory(dirname: str) -> str:
    """
    Init directory if not exist and return its path
    """
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname


def init_config() -> Dict[str, str]:
    """
    Read data from 'config.json' and return dictionary form its pairs
    """
    with open(os.path.join(os.getcwd(), "config.json")) as file:
        return json.load(file)


def init_style() -> str:
    """
    Read data from 'style.css' and return this data
    """
    with open(os.path.join(os.getcwd(), "gui", "style.css")) as styles:
        return styles.read()


def init_storing_directory() -> str:
    """
    Init and return direcotry for storing received files
    """
    config = init_config()
    directory = os.path.join(
        os.getcwd(),
        config.get("directory").get("main_dir"),
        config.get("directory").get("rec_dir"))
    return init_directory(directory)


def get_key(key_type: str):
    """
    key_type is public or private
    function returns key
    """
    config = init_config()
    directory = os.path.join(
        os.getcwd(),
        config.get("directory").get("main_dir"),
        config.get("directory").get("asym_dir"))
    directory = directory + f"\\{key_type}\\my_rsa_key"
    #if key_type == 'public': directory += ".pub"
    key = RSA.import_key(open(directory).read())
    return key


def save_public_key(key):
    """
    save received public key to dir
    """
    config = init_config()
    directory = os.path.join(
        os.getcwd(),
        config.get("directory").get("main_dir"),
        config.get("directory").get("rec_dir"))
    directory += "\\pub_key.key"
    with open(directory, "wb") as file:
        file.write(key.export_key())


def get_public_key():
    """
    get public key that was received from 2nd client
    """
    config = init_config()
    directory = os.path.join(
        os.getcwd(),
        config.get("directory").get("main_dir"),
        config.get("directory").get("rec_dir"))
    directory += "\\pub_key.key"
    key = RSA.import_key(open(directory).read())
    return key


