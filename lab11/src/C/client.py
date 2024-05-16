import socket

def main():
    host = '::1'  # IPv6 loopback address
    port = 50000

    client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message = input("Введите сообщение: ")
    client_socket.sendall(message.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Ответ от сервера: {response}")

    client_socket.close()

if __name__ == "__main__":
    main()
