"""
Module with functions to handle sending and receiving files by sockets
"""

import math
import ntpath
import os
import socket

from src.gui.progress_bar import ProgressBarDialog
from src.logic.utils.path import init_storing_directory

HEADER = 64
FORMAT = 'utf-8'
BUFFER_SIZE = 2048


def send_message_by(sender_socket: socket, text: str) -> bytes:
    """
    Send text using sockets
    """
    message_bytes = text.encode(FORMAT)
    bytes_count = len(message_bytes)
    enc_bytes_count = str(bytes_count).encode(FORMAT)
    enc_bytes_count += b' ' * (HEADER - len(enc_bytes_count))
    sender_socket.send(enc_bytes_count)
    sender_socket.send(message_bytes)
    return message_bytes


def receive_message_by(receive_socket: socket) -> str:
    """
    Get text from socket
    """
    message_length = receive_socket.recv(HEADER).decode(FORMAT)
    if message_length:
        message_value = receive_socket.recv(int(message_length)).decode(FORMAT)
        return message_value
    return ""


def send_file_by(sender_socket: socket, filename: str, buffer_size: int = 1024) -> None:
    """
    Send file using socket
    """
    base_filename = ntpath.basename(filename)
    send_message_by(sender_socket, base_filename)
    filepart_count = math.ceil(os.stat(filename).st_size / BUFFER_SIZE)
    send_message_by(sender_socket, str(filepart_count))
    pr = ProgressBarDialog(filepart_count)
    with open(filename, "rb") as f:
        for _ in range(filepart_count):
            pr.one_step_forward()
            bytes_read = f.read(buffer_size)
            sender_socket.sendall(bytes_read)


def receive_file_by(receive_socket, buffer_size: int = 1024) -> str:
    """
    Get file from socket
    """
    store_dir = init_storing_directory()
    filename = receive_message_by(receive_socket)
    filepart_count = int(receive_message_by(receive_socket))
    store_file = os.path.join(store_dir, filename)
    with open(store_file, "wb") as file:
        for _ in range(filepart_count):
            file.write(receive_socket.recv(buffer_size))
    return filename
