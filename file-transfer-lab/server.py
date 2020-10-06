#! /usr/bin/env python3

import sys, os
sys.path.append("../lib")       # for params
import re, socket, params

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

sock, addr = lsock.accept()

print("connection rec'd from", addr)


from framedSock import framedSend, framedReceive

# Retrieve file name and contents of file.
while True:
    file_name = framedReceive(sock, debug=1)
    if not file_name:
        framedSend(sock, "File name failure".encode(), debug=0)
        continue

    message = framedReceive(sock, debug=1)
    if not message:
        framedSend(sock, "Had trouble with contents of file".encode(), debug=0)
        continue

    # Checks if file exists
    if not os.path.exists(file_name.decode()):
        file = open("results/" + file_name.decode(), "wb")
    else:
        framedSend(sock, "File already found!".encode(), debug=1)

    # Writes to file.
    file.write(message)
    file.close()
    print("File closed.")

    framedSend(sock, "Success!".encode(), debug=0)
