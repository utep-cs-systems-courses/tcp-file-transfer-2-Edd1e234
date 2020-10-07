#!/usr/bin/env python3

import socket, sys, params, re
from framedSock import framedReceive

HOST = "127.0.0.1"
PORT = 50001
AMOUNT_OF_BYTES_TO_RECEIVE = 1024
DEBUG = 0
ERROR = "File how no contents"

def create_message(user_input):
    """
    Parse user command line arguments. Retrieve new file name. Retrive file contents.
    """
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

    if len(message) is 0:
        return ERROR, None

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


switchesVarDefaults = (
    (('-s', '--server'), 'server', HOST + ":" + str(PORT)),
    (('-d', '--debug'), "debug", DEBUG), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    (('-p', '--put'), "put", "local_file:remote_file"),
    )

progName = "framed_client"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

args = paramMap["put"].split(":")

# Checks if args parsed correctly.
if len(args) is not 2:
    print("Failed to parse")
    if DEBUG:
        print(args)
    sys.exit(1)


if DEBUG:
    print(args)
    print(args[0])


new_file_name, message = create_message(args[0] + " " + args[1])

if new_file_name is None:
    print("Failed to read file.")
    sys.exit(1)

if new_file_name == ERROR:
    print("File has no contents")
    sys.exit(1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((serverHost, serverPort))

    framedSend(s, new_file_name.encode(), debug=DEBUG)
    framedSend(s, message, debug=DEBUG)

    if DEBUG:
        print("Receving...")
    payload = framedReceive(s, DEBUG)
    print(payload.decode())
    sys.exit(1)
