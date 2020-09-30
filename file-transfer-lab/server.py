#!/usr/bin/env python3

import socket, os

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
AMOUNT_OF_BYTES_TO_RECEIVE = 1024
DEBUG = True


def create_file_name(file_name):
    list_file = file_name.split(".")
    return list_file[0] + "_created_by_server." + list_file[1]

def parse_inital_message(message_head):
    """
    Expecting message head to be file_name : file_length : message
    """
    message_split = message_head.split(" : ")

    if len(message_split) is not 3:
        return None

    try:
        file_name = message_split[0]
        file_length = int(message_split[1])
        file_message = message_split[2]
    except ValueError:
        return None
    return file_name, file_length, file_message

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

            # If no data is coming back end program.
            if not data:
                break
            decoded_messages = parse_inital_message(data.decode())

            # If None the message could not be parsed.
            if None != decoded_messages:
                print("Made it here.")
                file_name = decoded_messages[0]
                file_length = decoded_messages[1]
                file_message = decoded_messages[2]
                print(decoded_messages)

                # If file is empty do not create a file.
                if file_length is 0:
                    conn.sendall("Process failed, empty text".encode())
                    break

                # Create server file name.
                file_name = create_file_name(file_name)

                # If file does not exist create a file.
                FILE_DOES_NOT_EXISTS = False
                if not os.path.exists(file_name):
                    print("Hello world")
                    FILE_DOES_NOT_EXISTS = True
                    file = open(file_name, "w")

                amount_of_bytes = 0
                while True:
                    # print("Inside while loop")
                    for m in file_message:
                        print(m)
                        amount_of_bytes += 1
                        if FILE_DOES_NOT_EXISTS:
                            file.write(m)
                    # print("Made it passed the if.")
                     #print("amount_of_bytes: ", amount_of_bytes)
                    # print("file_name", file_length)

                    if amount_of_bytes is file_length:
                        break

                    # If file does not exists we still want to clear the payload.
                    file_message = conn.recv(AMOUNT_OF_BYTES_TO_RECEIVE).decode()

                    # Exit.
                    if not file_message:
                        break

                if FILE_DOES_NOT_EXISTS:
                    file.close()
                    conn.sendall("Process successful".encode())
                else:
                    conn.sendall("File already exists".encode())
