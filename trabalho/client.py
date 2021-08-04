#!/usr/bin/env python3
import json
import socket
import sys

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from diffieHellman import *

BLOCK_SIZE = 32

HOST = sys.argv[1] if len(sys.argv) > 2 else '127.0.0.1'  # The server's hostname or IP address
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 65432 # The port used by the server

private_key = rand_prime(1024)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))

  first_message = s.recv(1024)
  print(first_message.decode("utf-8"))

  data = s.recv(1024)
  jsonData = json.loads(data.decode())

  base = jsonData['base']
  shared_key = jsonData['shared_key']
  server_public_secret = jsonData['public_secret']

  public_secret = generate_public_secret(base, private_key, shared_key)
  shared_secret = generate_shared_secret(server_public_secret, private_key, shared_key)

  s.send(bytes(json.dumps({
    'public_secret': public_secret
  }), 'utf-8'))

  cipher = DES.new(shared_secret.to_bytes(8, byteorder='big'), DES.MODE_ECB)

  while True:
    message = input("Enter message: ")
    print('\n')

    if message == 'exit':
      print('Closing client')
      break
    else:
      print(f'Sending message: \"{message}\"')
      encrypted_message = cipher.encrypt(pad(bytes(message, 'utf-8'), BLOCK_SIZE))

      print(f'Encrypted message: \"{encrypted_message}\"')
      s.sendall(encrypted_message)
