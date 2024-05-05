import threading
import torch #pip install torch
import socket
import json
import logging
from cryptography.fernet import Fernet #pip install cryptography
from transformers import GPT2LMHeadModel, GPT2Tokenizer #pip install transformers
from encryption import get_env_key

# Load the configuration
with open('config.json') as f:
    config = json.load(f)

# Get the GPT2Server credentials from the configuration
host = config['GPT2Server']['host']
port = config['GPT2Server']['port']

# Generate a key and create a cipher object
key = get_env_key().encode()  # Call the get_env_key function and encode the result
cipher_suite = Fernet(key)

# Load the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# If CUDA is available, move the model to the GPU
# NOTE: CUDA is a parallel computing platform and application programming interface model created by NVIDIA
if torch.cuda.is_available():
    model = model.to('cuda')
    logging.info('Model moved to GPU')
else:
    logging.info('Model is running on CPU')

# Create a socket object
s = socket.socket()

# Bind the socket to a specific address and port
s.bind((host, port))

# Listen for incoming connections
s.listen(5)

running = False

print('Server is listening')

def server_thread():
    global running

    # Accept a connection
    c, addr = s.accept()
    print('Got connection from', addr)

    while running:
        try:
            # Receive a message, decrypt it, and print it
            encrypted_msg = c.recv(1024)

            decrypted_msg = cipher_suite.decrypt(encrypted_msg)
            print('Received message:', decrypted_msg.decode())

            # Process the message using the GPT-2 model
            input_ids = tokenizer.encode(decrypted_msg.decode(), return_tensors='pt')

            # If CUDA is available, move the input_ids tensor to the GPU
            if torch.cuda.is_available():
                input_ids = input_ids.to('cuda')

            attention_mask = torch.ones(input_ids.shape)
            output = model.generate(input_ids, max_length=50, num_return_sequences=1, temperature=0.7, do_sample=True, attention_mask=attention_mask)
            response = tokenizer.decode(output[0], skip_special_tokens=True)

            # Send the response
            encrypted_response = cipher_suite.encrypt(response.encode())
            c.send(encrypted_response)

        except socket.error:
            print('An error occurred:', socket.error)
            break

thread = threading.Thread(target=server_thread, daemon=True)

while True:
    print('GPT2Server: Available commands: start, exit')
    command = input()
    if command.lower() == 'start':
        if not thread.is_alive():
            running = True
            thread.start()
            print('Server is listening')
    elif command.lower() == 'exit':
        if thread.is_alive():
            running = False
            s.close()
            print('Server has stopped')
        print('Exiting program')
        break