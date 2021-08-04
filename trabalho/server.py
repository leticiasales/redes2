#!/usr/bin/env python3
import socket
import sys

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 65432 # Port to listen on

if PORT > 1023: print('Using port', PORT)
else: sys.exit('Please enter a valid port (non-privileged ports are > 1023)')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try: s.bind((HOST, PORT))
    except Exception as err: sys.exit(f'Error creating server: {err}')
    
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)