import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)
sock.settimeout(1)

rtts = []
lost_packets = 0

for i in range(1, 11):
    message = f'Ping {i} {time.time()}'
    try:
        sent = sock.sendto(message.encode('utf-8'), server_address)
        data, server = sock.recvfrom(4096)
        rtt = time.time() - float(message.split()[2])
        rtts.append(rtt)
        print(f'{data.decode("utf-8")} RTT={rtt} sec')
    except socket.timeout:
        lost_packets += 1
        print('Request timed out')

    min_rtt = min(rtts) if rtts else 0
    max_rtt = max(rtts) if rtts else 0
    avg_rtt = sum(rtts) / len(rtts) if rtts else 0
    packet_loss = (lost_packets / 10) * 100
    print(f'{i} packets transmitted, {len(rtts)} received, {packet_loss:.0f}% packet loss')
    print(f'rtt min/avg/max = {min_rtt:.3f}/{avg_rtt:.3f}/{max_rtt:.3f}')
    print()

