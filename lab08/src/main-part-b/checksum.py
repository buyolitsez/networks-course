def calculate_checksum(data):
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

def verify_checksum(data, checksum):
    calculated_checksum = calculate_checksum(data)
    return calculated_checksum == checksum
