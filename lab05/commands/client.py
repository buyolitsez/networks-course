import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

command = input()
client_socket.send(command.encode('utf-8'))

result = client_socket.recv(1024).decode('utf-8')
print('result:', result)
