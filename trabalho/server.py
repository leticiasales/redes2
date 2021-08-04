#!/usr/bin/env python3
import json
import socket
import sys

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from diffieHellman import *

BLOCK_SIZE = 32

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 65432 # Port to listen on

if PORT > 1023: print('Using server port:', PORT)
else: sys.exit('Please enter a valid port (non-privileged ports are > 1023)')

base, private_key, shared_key = rand_prime(255), rand_prime(255), rand_prime(255)
# Generate random prime values for a, g and p

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  try: s.bind((HOST, PORT))
  except Exception as err: sys.exit(f'Error creating server: {err}')

  s.listen()
  print('Awaiting client connection...')

  conn, (client_host, client_port) = s.accept()  

  with conn:
    print(f'Connected by {client_host}:{client_port}')

    conn.send(bytes('Beginning Diffie-Hellman key exchange.', 'utf-8'))

    public_secret = generate_public_secret(base, private_key, shared_key)

    conn.send(bytes(json.dumps({
      'base': base,
      'shared_key': shared_key,
      'public_secret': public_secret
      }), 'utf-8'))

    data = conn.recv(1024)

    client_public_secret = json.loads(data.decode())['public_secret']
    shared_secret = generate_shared_secret(client_public_secret, private_key, shared_key)
    cipher = DES.new(shared_secret.to_bytes(8, byteorder='big'), DES.MODE_ECB)

    while True:
      data = conn.recv(1024)

      if not data:
        break
      else:
        decrypted_data = unpad(cipher.decrypt(data), BLOCK_SIZE).decode('utf-8')

        print(f'Received message: \"{decrypted_data}\"')
