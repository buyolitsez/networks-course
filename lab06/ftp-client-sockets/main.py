import socket
import argparse

def receive_response(s):
    while True:
        response = s.recv(4096).decode()
        if response[3] == ' ':
            return response

def ftp_client(server, username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((server, 21))

    client_socket.sendall(f'USER {username}\r\n'.encode())
    print(receive_response(client_socket))

    client_socket.sendall(f'PASS {password}\r\n'.encode())
    print(receive_response(client_socket))

    client_socket.sendall(b'PORT 21\r\n')
    print(receive_response(client_socket))

    print("Файлы на сервере")
    client_socket.sendall(b'LIST\r\n')
    print(receive_response(client_socket))

    print('Загружаем файл send.txt')
    client_socket.sendall(b'STOR send.txt\r\n')
    print(receive_response(client_socket))

    print('Скачиваем файл format.sh')
    client_socket.sendall(b'RETR format.sh\r\n')
    print(receive_response(client_socket))

    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FTP client')
    parser.add_argument('--server', type=str, required=True)
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)

    args = parser.parse_args()

    ftp_client(args.server, args.username, args.password)
