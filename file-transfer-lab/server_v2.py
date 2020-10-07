#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os
DEBUG = False

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)

        # Retrive files names.
        file_name = framedReceive(sock, debug=DEBUG)
        if not file_name:
            framedSend(sock, "File name failure".encode(), debug=DEBUG)
            sys.exit(1)

        message = framedReceive(sock, debug=DEBUG)
        if not message:
            framedSend(sock, "Had trouble with contents of file".encode(), debug=DEBUG)
            sys.exit(1)

        # Checks if file exists
        if not os.path.exists("results/" + file_name.decode()):
            file = open("results/" + file_name.decode(), "w+b")
        else:
            framedSend(sock, "File already found!".encode(), debug=DEBUG)
            sys.exit(1)

        # Writes to file.
        file.write(message)
        file.close()
        print("File closed. Success!")
        framedSend(sock, "Success!".encode(), debug=DEBUG)
        sys.exit(1)
