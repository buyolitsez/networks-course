import tkinter as tk
import socket

root = tk.Tk()
root.title("Удаленное рисование (клиент)")
canvas = tk.Canvas(root, bg="white", width=400, height=400)
canvas.pack()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12347))

def on_mouse_move(event):
    x, y = event.x, event.y
    client_socket.send(f"{x},{y}".encode())
    canvas.create_oval(x - 2, y - 2, x+2, y+2, fill="black")

canvas.bind("<B1-Motion>", on_mouse_move)

root.mainloop()

client_socket.close()
