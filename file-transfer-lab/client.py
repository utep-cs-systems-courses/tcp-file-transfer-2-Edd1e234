#!/usr/bin/env python3

import socket, sys
from framedSock import framedReceive

HOST = "127.0.0.1"
PORT = 50001
AMOUNT_OF_BYTES_TO_RECEIVE = 1024
DEBUG = True


import re

def create_message(user_input):
    if len(user_input) is 0:
        return None

    messages = user_input.split(" ")

    if len(messages) is not 2:
        return None

    file_name = messages[0]
    new_file_name = messages[1]

    try:
        actual_file = open(file_name, "rb")
    except FileNotFoundError:
        print("FileNotFoundError")
        return None

    data = actual_file.read(1024*1024)
    message = b""
    while data:
        message += data
        data = actual_file.read(1024*1024)

    return new_file_name, message


def framedSend(sock, payload, debug=0):
    # Debug statements.
    if debug:
        print("framedSend: sending %d byte message" % len(payload))
    if debug:
        print(payload)

    msg = str(len(payload)).encode() + b':' + payload
    while len(msg):
        nsent = sock.send(msg)
        msg = msg[nsent:]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Change the port number.
    if len(sys.argv) is 3:
        if "-p" in sys.argv:
            PORT = int(sys.argv[2])
        else:
            print("Command line arguments do ")

    s.connect((HOST, PORT))

    print("Type exit to end connection")
    while True:
        user_input = input("Enter file name and remote file name: ")

        if not user_input:
            continue

        # End program.
        if user_input == "exit":
            break

        if DEBUG:
            print("Sending...")


        print("Sending...")
        new_file_name, message = create_message(user_input)
        framedSend(s, new_file_name.encode(), debug=1)
        framedSend(s, message, debug=1)

        if DEBUG:
            print("Receving...")
        framedReceive(s, DEBUG)
