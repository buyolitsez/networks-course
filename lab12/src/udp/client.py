# client.py
import socket
import random
import time
import tkinter as tk
import struct

def send_packets(ip, port, num_packets):
    server_address = (ip, port)
    client_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_tcp.connect(server_address)
    client_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    start_time = time.time()

    header = struct.pack("d", time.time()) + struct.pack("q", num_packets)
    print('header = ', header, " len = ", len(header))

    client_socket_tcp.sendall(header)

    for _ in range(num_packets):
        client_socket_udp.sendto(random.randbytes(2048), server_address)



def send_button_click():
    ip = ip_entry.get()
    port = int(port_entry.get())
    num_packets = int(num_packets_entry.get())
    send_packets(ip, port, num_packets)

# GUI setup
root = tk.Tk()
root.title("TCP Client")
ip_label = tk.Label(root, text="IP адрес получателя:")
ip_entry = tk.Entry(root)
port_label = tk.Label(root, text="Порт отправки:")
port_entry = tk.Entry(root)
num_packets_label = tk.Label(root, text="Количество пакетов:")
num_packets_entry = tk.Entry(root)
send_button = tk.Button(root, text="Отправить", command=send_button_click)

ip_label.pack()
ip_entry.pack()
port_label.pack()
port_entry.pack()
num_packets_label.pack()
num_packets_entry.pack()
send_button.pack()

root.mainloop()
