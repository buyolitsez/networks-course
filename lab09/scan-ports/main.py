import socket
import sys

def scan_ports(ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

if __name__ == "__main__":
    ip = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    open_ports = scan_ports(ip, start_port, end_port)
    print("ports:")
    for port in open_ports:
        print(port)
