#!/usr/bin/env python3

import socket, sys

HOST = "127.0.0.1"
PORT = 65432
AMOUNT_OF_BYTES_TO_RECEIVE = 1024

def create_message(file_name):
    if len(file_name) is 0:
        return None

    try:
        actual_file = open(file_name, "r")
    except FileNotFoundError:
        print("FileNotFoundError")
        return None

    message = ""

    for line in actual_file:
        message += line


    return file_name + " : " + str(len(message)) + " : " + message

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
        file_name = input("Enter file name: ")

        # End program.
        if file_name == "exit":
            break
        message = create_message(file_name)
        if message == None:
            print("Failed to parse, try again.\n")
            continue

        s.sendall(message.encode())
        data = s.recv(AMOUNT_OF_BYTES_TO_RECEIVE)

        print("Received: ", data.decode())
