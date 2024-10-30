import select
import socket
import sys
import threading
from des import decryption, encryption

class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080
        self.threads = []

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(3)

    def run(self):
        self.open_socket()
        input_list = [self.server]
        while 1:
            read_ready, write_ready, exception = select.select(input_list, [], [])
            for r in read_ready:
                if r == self.server:
                    client_socket, client_address = self.server.accept()
                    print("Sudah terhubung dengan klien")
                    c = Client(client_socket, client_address, input_list)
                    c.start()
                    self.threads.append(c)
        self.server.close()

        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self, client, address, input_list):
        threading.Thread.__init__(self)
        self.sock = client
        self.SOCKET_LIST = input_list
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        try:
            while 1:
                data = self.client.recv(self.size)
                if data:
                    data = data.decode('utf-8')
                    print(f"\nCiphertext : {data}")
                    decrypted = decryption(data)
                    print(f"Decrypted Text: {decrypted}\n")

                    print("Masukkan Pesan:")
                    response = input()
                    encrypted_response = encryption(response)
                    self.client.send(encrypted_response.encode('utf-8'))
                else:
                    self.client.close()
        except:
            if self.sock in self.SOCKET_LIST:
                self.SOCKET_LIST.remove(self.sock)

            print("Klien tidak ditemukan")
            self.client.close()

if __name__ == "__main__":
    try:
        server = Server()
        server.run()
    except KeyboardInterrupt:
        sys.exit(0)
