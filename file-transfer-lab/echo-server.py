#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
AMOUNT_OF_BYTES_TO_RECEIVE = 1024
DEBUG = True

# socket.socket() creates a socket object that supports the context manager
#   type.
# The argument passed to socket() specify the address family and socket type.
# AF_INET is the Internet address family for IPv4.SOCK_STREAM is the socket type
#   TCP, the protocal that will be used to transport our messages in the
#   network.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # bind() is used to associate the socket with a specific network interface
    #   and port number.
    # Host can be a Hostname, IP address, or empty string
    s.bind((HOST, PORT))
    s.listen()  # Enables the server to accept connections.

    # Waits for incoming connection.
    # Returns object representing the connection and a tuble holding the address
    #   of the client.
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            # Reads whatever the client is sending.
            data = conn.recv(AMOUNT_OF_BYTES_TO_RECEIVE)
            if not data:
                break

            data = data.decode()
            if ":" in data:
                data_split = data.split(":")
                file = open(data_split[0]+"_created_by_server", "w")
                file_doc = data_split[1]   # Actual text in doc.

                CONTAINS_DATA = True # if there is no more data end.

                while True:
                    for char in file_doc:
                        if DEBUG:
                            print("In for loop")
                            print(char)

                        if char == ">":
                            CONTAINS_DATA = False
                            break
                        file.write(char)

                    if CONTAINS_DATA:
                        file_doc = conn.recv(AMOUNT_OF_BYTES_TO_RECEIVE).decode()
                    else:
                        print("Hello")
                        break

                file.close()
            print("File has been closed.")
            # Echos the data back.
            conn.sendall("Process successful".encode())
