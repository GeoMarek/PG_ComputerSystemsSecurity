"""
Module with functions to handle sending and receiving files by sockets
"""

import math
import ntpath
import os
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from src.gui.progress_bar import ProgressBarDialog
from src.logic.utils.path import init_storing_directory, get_public_key, get_key

from src.logic.encrypter import Encrypter

HEADER = 64
FORMAT = 'utf-8'
BUFFER_SIZE = 2048
encrypter = Encrypter()


def send_key(s: socket, key):
    if "<class 'Crypto.PublicKey.RSA.RsaKey'>" == str((type(key))):
        key = key.exportKey("PEM")
        s.send(b'1')
    else: s.send(b'0')
    key_len = len(key)
    enc_key_len = str(key_len).encode(FORMAT)
    enc_key_len += b' ' * (HEADER - len(enc_key_len))
    s.send(enc_key_len)
    s.send(key)


def rec_key(s: socket):
    convert = False
    if s.recv(1) == b'1':
        convert = True
    key_len = s.recv(HEADER).decode(FORMAT)
    key = s.recv(int(key_len))
    if convert:
        key = RSA.importKey(key)
    return key


def stuff_send_session_key(s: socket):
    session_key = encrypter.generate_session_key()
    pub_key = get_public_key()
    cipher_rsa = PKCS1_OAEP.new(pub_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    send_key(s, enc_session_key)
    return session_key


def stuff_rec_session_key(s: socket):
    enc_session_key = rec_key(s)
    private_key = get_key('private')
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)
    return session_key


def send_message_by(sender_socket: socket, text: str, mode: str = 'CBC') -> bytes:
    """
    Send text using sockets
    """
    key = stuff_send_session_key(sender_socket)
    message_bytes = encrypter.encrypt_msg(text, mode, key)
    bytes_count = len(message_bytes)
    enc_bytes_count = str(bytes_count).encode(FORMAT)
    enc_bytes_count += b' ' * (HEADER - len(enc_bytes_count))
    sender_socket.send(enc_bytes_count)
    sender_socket.send(mode.encode(FORMAT))
    sender_socket.send(message_bytes)
    return message_bytes


def receive_message_by(receive_socket: socket) -> str:
    """
    Get text from socket
    """
    key = stuff_rec_session_key(receive_socket)
    message_length = receive_socket.recv(HEADER).decode(FORMAT)
    if message_length:
        mode = receive_socket.recv(3).decode(FORMAT)
        message_value = receive_socket.recv(int(message_length))
        return encrypter.decrypt_msg(message_value, mode, key)
    return ""


def send_file_by(sender_socket: socket, filename: str, mode: str = 'CBC', buffer_size: int = 1024) -> None:
    """
    Send file using socket
    """
    key = stuff_send_session_key(sender_socket)
    file = encrypter.encrypt_fun(filename, mode, key)
    base_filename = ntpath.basename(file)
    send_message_by(sender_socket, base_filename)
    filepart_count = math.ceil(os.stat(file).st_size / BUFFER_SIZE)
    send_message_by(sender_socket, str(filepart_count))
    sender_socket.send(mode.encode(FORMAT))
    pr = ProgressBarDialog(filepart_count)
    with open(file, "rb") as f:
        for _ in range(filepart_count):
            pr.one_step_forward()
            bytes_read = f.read(buffer_size)
            sender_socket.sendall(bytes_read)


def receive_file_by(receive_socket, buffer_size: int = 1024) -> str:
    """
    Get file from socket
    """
    key = stuff_rec_session_key(receive_socket)
    store_dir = init_storing_directory()
    filename = receive_message_by(receive_socket)
    filepart_count = int(receive_message_by(receive_socket))
    mode = receive_socket.recv(3).decode(FORMAT)
    store_file = os.path.join(store_dir, filename)
    with open(store_file, "wb") as file:
        for _ in range(filepart_count):
            file.write(receive_socket.recv(buffer_size))
    encrypter.decrypt_fun(f"{store_dir}\\{filename}", mode, key)
    return filename
