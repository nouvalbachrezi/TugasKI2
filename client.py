import socket
import sys
from des import encryption, decryption

class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080

    def open_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def run(self):
        self.open_socket()
        while True:
            print("Masukkan Pesan:")
            msg = input()
            encrypted_msg = encryption(msg)
            self.client.send(encrypted_msg.encode('utf-8'))

            # Receive encrypted message from server
            encrypted_response = self.client.recv(1024).decode('utf-8')
            print(f"\nCiphertext: {encrypted_response}")

            decrypted_response = decryption(encrypted_response)
            print(f"Decrypted Text: {decrypted_response}\n")

if __name__ == "__main__":
    client = Client()
    client.run()
