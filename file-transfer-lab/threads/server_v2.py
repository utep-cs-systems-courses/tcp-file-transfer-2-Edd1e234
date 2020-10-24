#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os, threading, time
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

from threading import Thread
from framedSock import framedSend, framedReceive

# Lock object
thread_lock = threading.Lock()

# Contains files.
active_files = set()

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr

    def run(self):
        """
        First get file name. Check if exists, if not get the rest of the
        file contents.
        """
        if DEBUG:
            time.sleep(5)

        print("New thread handling connection from", self.addr)

        file_name = framedReceive(self.sock, debug=DEBUG)
        if not file_name:
            framedSend(self.sock, "File name not found".encode(), debug=DEBUG)
            return

        file_name = "results/" + file_name.decode()

        # lock thread, to begin writing file.
        thread_lock.acquire()
        if not os.path.exists(file_name) and file_name not in active_files:
            file = open(file_name, "w+b")
            active_files.add(file_name)

        else:
            framedSend(self.sock, "File already found!".encode(), debug=DEBUG)

            # Do nothing.
            return
        thread_lock.release()

        message = framedReceive(self.sock, debug=DEBUG)
        if not message:
            framedSend(self.sock, "Had trouble with contents of file".encode(), debug=DEBUG)
            return

        # Finish file operation.
        file.write(message)
        file.close()

        # Remove from active_files
        thread_lock.acquire()
        active_files.remove(file_name)
        thread_lock.release()

        print("File closed. Success!")
        framedSend(self.sock, "Success".encode(), debug=DEBUG)

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)

    server.start()
