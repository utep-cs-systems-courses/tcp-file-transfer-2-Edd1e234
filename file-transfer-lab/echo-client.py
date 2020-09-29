#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"
PORT = 65432
AMOUNT_OF_BYTES_TO_RECEIVE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        print("Type exit to end connection")
        value = input("Enter file name: ")

        # End program.
        if value == "exit":
            break

        try:
            file = open(value, "r")
        except FileNotFoundError:
            print("File not foud.")
            pass

        fileContent = ""
        for x in file:
            fileContent += x

        value = value + ":<" + fileContent

        s.sendall(value.encode())
        data = s.recv(AMOUNT_OF_BYTES_TO_RECEIVE)

        print("Received", repr(data))
