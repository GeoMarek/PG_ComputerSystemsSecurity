"""
Module with functions to hash data with sha256
"""
from hashlib import sha256


def get_hash_from(text: str) -> bytearray:
    encoded_text = text.encode('utf-8')
    hashed_text = sha256(encoded_text)
    return bytearray(hashed_text.digest())
