# server.py
import socket
import time
import tkinter as tk
import struct
import tkinter.messagebox

def receive_packets(ip, port):
    global T
    server_address = (ip, port)
    server_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_tcp.bind(server_address)
    server_socket_tcp.listen()

    print(f"Сервер слушает на {ip}:{port}")

    total_bytes_received = 0
    packages_received = 0

    connection, _ = server_socket_tcp.accept()
    data = connection.recv(16)
    start_time = struct.unpack_from("d", data[0:8])[0]
    num_packets = struct.unpack_from("q", data[8:16])[0]

    server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket_udp.bind(server_address)
    server_socket_udp.settimeout(1)
    try:
        for _ in range(num_packets):
            data = server_socket_udp.recv(2048)
            total_bytes_received += len(data)
            packages_received += 1
    except socket.timeout:
        pass

    for _ in range(num_packets):
        data = connection.recv(2048)
        total_bytes_received += len(data)

    end_time = time.time()
    elapsed_time = end_time - start_time
    speed = total_bytes_received / elapsed_time
    T.insert(tk.END, "---------------\n")
    T.insert(tk.END, f"Получено {total_bytes_received} байт за {elapsed_time:.2f} секунд\n")
    T.insert(tk.END, f"Скорость передачи: {speed:.2f} байт/сек\n")
    T.insert(tk.END, f"Получено пакетов: {packages_received}\n")

# GUI setup
root = tk.Tk()
root.title("TCP Server")
ip_label = tk.Label(root, text="IP адрес:")
ip_entry = tk.Entry(root)
port_label = tk.Label(root, text="Порт получения:")
port_entry = tk.Entry(root)
receive_button = tk.Button(root, text="Получить", command=lambda: receive_packets(ip_entry.get(), int(port_entry.get())))
T = tk.Text(root, height = 5, width = 52)

ip_label.pack()
ip_entry.pack()
port_label.pack()
port_entry.pack()
T.pack()
receive_button.pack()

root.mainloop()
