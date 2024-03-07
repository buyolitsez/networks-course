import socket
import threading
import os
import sys

class ThreadedServer:
    def __init__(self, host, port, concurrency_level):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.semaphore = threading.Semaphore(concurrency_level)

    def start(self):
        self.server.listen()
        print(f"started: {self.host}:{self.port}")
        while True:
            client, address = self.server.accept()
            self.semaphore.acquire()
            threading.Thread(target=self.handle_client, args=(client, address)).start()

    def handle_client(self, client, address):
        print(f"connection: {address}")
        data = client.recv(1024).decode()
        filename = self.get_filename_from_http_request(data)
        if filename and os.path.exists(filename):
            with open(filename, 'r') as file:
                response = self.construct_http_response(200, 'OK', file.read())
        else:
            response = self.construct_http_response(404, 'Not Found', '404 Not Found')
        client.send(response.encode())
        client.close()
        self.semaphore.release()

    def get_filename_from_http_request(self, request):
        try:
            return request.split(' ')[1][1:]
        except IndexError:
            return None

    def construct_http_response(self, status_code, status_message, content):
        return f"HTTP/1.1 {status_code} {status_message}\r\n\r\n{content}"

if __name__ == "__main__":
    server_port = int(sys.argv[1])
    concurrency_level = int(sys.argv[2])
    server = ThreadedServer('localhost', server_port, concurrency_level)
    server.start()

