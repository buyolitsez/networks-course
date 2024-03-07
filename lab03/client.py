import socket
import sys

class HttpClient:
    def __init__(self, server_host, server_port, filename):
        self.server_host = server_host
        self.server_port = server_port
        self.filename = filename

    def start(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_host, self.server_port))

        request = f"GET /{self.filename} HTTP/1.1\r\nHost: {self.server_host}\r\n\r\n"
        client_socket.send(request.encode())

        response = client_socket.recv(1024)
        print(response.decode())

        client_socket.close()

if __name__ == "__main__":
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]
    client = HttpClient(server_host, server_port, filename)
    client.start()
