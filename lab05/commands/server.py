import socket
import subprocess

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

while True:
    client_socket, addr = server_socket.accept()
    print('connection:', addr)

    # Получаем команду от клиента
    command = client_socket.recv(1024).decode('utf-8')
    print('command:', command)

    # Выполняем команду и отправляем каждую строку вывода обратно клиенту
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout:
        client_socket.send(line)
