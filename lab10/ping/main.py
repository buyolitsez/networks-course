import os
import socket
import struct
import select
import time
import argparse

def checksum(data):
    if len(data) % 2 != 0:
        data += b'\0'

    checksum = 0
    for i in range(0, len(data), 2):
        word = data[i] + (data[i+1] << 8)
        checksum += word

    while (checksum >> 16) > 0:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    checksum = ~checksum & 0xFFFF

    return checksum

def create_packet(id):
    header = struct.pack('>BBHHH', 8, 0, 0, id, 1)
    header = struct.pack('>BBHHH', 8, 0, checksum(header), id, 1)
    return header

def do_one(dest_addr, timeout):
    icmp = socket.getprotobyname('icmp')
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error as e:
        if e.errno == 1:
            msg = 'run as root'
            raise socket.error(msg)
        raise
    my_ID = os.getpid() & 0xFFFF
    send_one_ping(my_socket, dest_addr, my_ID)
    delay = receive_one_ping(my_socket, timeout, time.time())
    my_socket.close()
    return delay

def send_one_ping(my_socket, dest_addr, ID):
    packet = create_packet(ID)
    my_socket.sendto(packet, (dest_addr, 1))

def receive_one_ping(my_socket, timeout, time_sent):
    my_socket.settimeout(timeout)
    try:
        my_socket.recvfrom(1024)
        delay = time.time() - time_sent
    except socket.timeout:
        delay = None

    return delay

def verbose_ping(dest_addr, timeout = 1, count = 10):
    min_rtt = None
    max_rtt = None
    sum_rtt = 0
    lost_packets = 0

    for i in range(1, count + 1):
        time.sleep(1)
        print('ping {}...'.format(dest_addr))
        delay = do_one(dest_addr, timeout)
        if delay == None:
            print('failed. (Timeout within {} seconds.)'.format(timeout))
            lost_packets += 1
        else:
            delay = delay * 1000
            print('get ping in {:.1f} milliseconds.'.format(delay))
            if min_rtt is None or delay < min_rtt:
                min_rtt = delay
            if max_rtt is None or delay > max_rtt:
                max_rtt = delay
            sum_rtt += delay
        if min_rtt is not None and max_rtt is not None:
            avg_rtt = sum_rtt / i
            loss_percent = (lost_packets / i) * 100
            print('min/avg/max = {:.1f}/{:.1f}/{:.1f} ms, loss = {:.1f}%'.format(min_rtt, avg_rtt, max_rtt, loss_percent))

    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ping a host.')
    parser.add_argument('host', type=str, help='The host to ping.')
    args = parser.parse_args()
    verbose_ping(args.host)
