import tkinter as tk
import socket
import threading

root = tk.Tk()
root.title("Удаленное рисование (сервер)")
canvas = tk.Canvas(root, bg="white", width=400, height=400)
canvas.pack()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12347))
server_socket.listen()

client_socket, client_address = server_socket.accept()

def update_canvas():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            x, y = map(int, data.split(","))
            canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
        except Exception as e:
            print('error = ', e)

receive_thread = threading.Thread(target=update_canvas)
receive_thread.daemon = True
receive_thread.start()
root.mainloop()

server_socket.close()
