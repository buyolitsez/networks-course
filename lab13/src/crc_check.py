import argparse
import random

POLYNOMIAL = 0x1021
PRESET = 0xFFFF

def crc16(data: bytes):
    crc = PRESET
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ POLYNOMIAL
            else:
                crc = crc << 1
            crc &= 0xFFFF
    return crc

class Packet:
    def __init__(self, data: bytes):
        self.data = data
        self.crc = self.calculate_crc()

    def calculate_crc(self):
        return crc16(self.data)

    def encode_packet(self):
        return self.data + self.crc.to_bytes(2, byteorder='big')

    @staticmethod
    def decode_packet(packet_bytes: bytes):
        data = packet_bytes[:-2]
        crc = int.from_bytes(packet_bytes[-2:], byteorder='big')
        return data, crc

    @staticmethod
    def verify_packet(packet_bytes: bytes):
        data, received_crc = Packet.decode_packet(packet_bytes)
        calculated_crc = crc16(data)
        return calculated_crc == received_crc

def introduce_error(packet_bytes: bytes):
    error_index = random.randint(0, len(packet_bytes) - 1)
    error_byte = packet_bytes[error_index] ^ 0xFF
    return packet_bytes[:error_index] + bytes([error_byte]) + packet_bytes[error_index + 1:]

def main(input_text: str):
    packet_length = 5
    input_bytes = input_text.encode('utf-8')
    packets = [Packet(input_bytes[i:i+packet_length]) for i in range(0, len(input_bytes), packet_length)]
    
    encoded_packets = [packet.encode_packet() for packet in packets]

    print("Original Packets:")
    print(f"{'Index':<5}{'Data':<15}{'Encoded':<30}{'CRC':<10}")
    for i, packet in enumerate(packets):
        print(f"{i:<5}{packet.data!s:<15}{packet.encode_packet()!s:<30}{packet.crc:<10}")

    encoded_packets_with_errors = [introduce_error(packet) if random.random() < 0.5 else packet for packet in encoded_packets]

    print("\nPackets with Potential Errors:")
    print(f"{'Index':<5}{'Data':<15}{'Encoded':<30}{'CRC':<10}")
    for i, packet_bytes in enumerate(encoded_packets_with_errors):
        data, crc = Packet.decode_packet(packet_bytes)
        print(f"{i:<5}{data!s:<15}{packet_bytes!s:<30}{crc:<10}")

    print("\nPacket Verification:")
    for i, packet_bytes in enumerate(encoded_packets_with_errors):
        if Packet.verify_packet(packet_bytes):
            print(f"Packet {i}: No error")
        else:
            print(f"Packet {i}: Error detected")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CRC Packet Integrity Check")
    parser.add_argument("input_text", type=str, help="Input text to be split into packets and checked for integrity")
    args = parser.parse_args()
    main(args.input_text)
