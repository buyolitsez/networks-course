import socket
import struct
import time
import argparse
import os

def checksum(data):
    if len(data) % 2:
        data += b'\x00'
    sum = 0
    for i in range(0, len(data), 2):
        sum += (data[i] << 8) + data[i+1]
    while (sum >> 16):
        sum = (sum & 0xFFFF) + (sum >> 16)
    sum = ~sum & 0xFFFF
    return sum

def hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        return None

packet_num = 0

def create_packet(id):
    global packet_num
    data = b""
    header = struct.pack("!BBHHH", 8, 0, 0, 0, packet_num)
    header = struct.pack("!BBHHH", 8, 0, checksum(header + data), 0, packet_num)
    packet_num += 1
    return header + data

def main(target_host, max_hops=30, timeout=2):
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.settimeout(timeout)
    break_flag = False
    
    for ttl in range(1, max_hops + 1):
        if break_flag:
            break
        icmp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

        icmp_socket.sendto(create_packet(42), (target_host, 0))
        start_time = time.time()

        try:
            data, addr = icmp_socket.recvfrom(1024)
            end_time = time.time()
            ip_address = addr[0]
            rtt = (end_time - start_time) * 1000
            host = hostname(addr[0])
            if host is not None:
                print(f"Hop {ttl}: {ip_address} [{host}] (RTT: {rtt:.2f} ms)")
            else:
                print(f"Hop {ttl}: {ip_address} (RTT: {rtt:.2f} ms)")
            if (data[20] == 0):
                break_flag = True
        except socket.timeout:
            print(f"Hop {ttl}: * (Timeout)")
    
    icmp_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ICMP Traceroute")
    parser.add_argument("target_host", help="Целевой хост для трассировки")
    parser.add_argument("--max_hops", type=int, default=30, help="Максимальное количество шагов (по умолчанию: 30)")
    parser.add_argument("--timeout", type=int, default=2, help="Таймаут ожидания ответа (по умолчанию: 2 секунды)")
    args = parser.parse_args()
    
    main(args.target_host, args.max_hops, args.timeout)
