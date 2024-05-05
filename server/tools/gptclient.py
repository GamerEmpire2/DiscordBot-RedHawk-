import socket
import os
import json
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from encryption import get_env_key

load_dotenv()
env_root = os.getenv('PROJECT_ROOT')

# Load the configuration
with open(os.path.join(env_root, 'config.json')) as f:
    config = json.load(f)

# Get the GPT2Server credentials from the configuration
host = config['GPT2Server']['host']
port = config['GPT2Server']['port']

# Generate a key and create a cipher object
key = get_env_key().encode()  # Call the get_env_key function and encode the result
cipher_suite = Fernet(key)

# Create a socket object
s = socket.socket()

# Connect to the server
s.connect((host, port))

while True:
    msg = input("Enter a message to send (or exit): ")
    if msg.lower() == 'exit':
        s.close()
        break

    # Encrypt the message and send it to gpt server
    encrypted_msg = cipher_suite.encrypt(msg.encode())
    s.send(encrypted_msg)
    encrypted_response = s.recv(1024)
    decrypted_response = cipher_suite.decrypt(encrypted_response)
    print("Received response:", decrypted_response.decode())
