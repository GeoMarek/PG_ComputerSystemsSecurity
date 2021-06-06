import socket, sys
import threading
import os
import math

HEADER = 64
FORMAT = 'utf-8'
BUFFER_SIZE = 8

def send_msg(sender, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    sender.send(send_length)
    sender.send(message)

def recive_msg(connection):
    msg_length = connection.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = connection.recv(msg_length).decode(FORMAT)
        print(f"{msg}")
    return msg

def send_file(s, file_name):
    send_msg(s, file_name)
    reps = math.ceil(os.stat(file_name).st_size / BUFFER_SIZE)
    send_msg(s,str(reps))
    with open(file_name, "rb") as f:
        for x in range(reps):
            bytes_read = f.read(BUFFER_SIZE)
            s.sendall(bytes_read)
    print("wyslano plik")

def recive_file(s):
    file_name = recive_msg(s)
    i = int(recive_msg(s))
    with open(file_name, "wb") as f:
        for x in range(i):
            bytes_read = s.recv(BUFFER_SIZE)
            f.write(bytes_read)
    print("odebrano plik")

def loop_of_sends(s):
    while True:
        send_type = input()
        if send_type == "file":
            print("sending file. What file name? ")
            s.sendall("f".encode(FORMAT))
            file_name = input()
            send_file(s, file_name)
        elif send_type == "msg":
            print("sending msg. What to send? ")
            s.sendall("m".encode(FORMAT))
            msg = input()
            send_msg(s, msg)
        else:
            print("incorect send type")

def loop_of_recives(s):
    while True:
        recive_type = s.recv(HEADER).decode(FORMAT)
        if recive_type == "f":
            print("odbieramy plik")
            recive_file(s)
        elif recive_type == "m":
            print("odbieramy wiadomosc")
            recive_msg(s)
        else:
            print(f"co to ma byc? {recive_type}")

def handle_connection(s):
    thread_send = threading.Thread(target=loop_of_sends, args=(s,))
    thread_rec = threading.Thread(target=loop_of_recives, args=(s,))
    thread_rec.start()
    thread_send.start()