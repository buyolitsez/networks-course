import socket

def main():
    host = '::1'
    port = 50000

    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Подключение от {client_address}")

        data = client_socket.recv(1024).decode('utf-8')
        if data:
            response = data.upper()
            client_socket.sendall(response.encode('utf-8'))

        client_socket.close()

if __name__ == "__main__":
    main()
