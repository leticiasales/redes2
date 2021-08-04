#!/usr/bin/env python3
import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 2 else '127.0.0.1'  # The server's hostname or IP address
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 65432 # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))

  message = sys.argv[3] if len(sys.argv) > 2 \
    else sys.argv[1] if len(sys.argv) > 1 \
    else input("Enter message: ")

  s.sendall(bytes(message, 'utf-8'))
  data = s.recv(1024)

  print('Received', data.decode('utf-8'))