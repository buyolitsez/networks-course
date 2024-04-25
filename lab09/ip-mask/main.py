import subprocess
import re

def parse_ifconfig():
    result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE)
    ifconfig_output = result.stdout.decode()

    pattern = r'(\w+):.*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?netmask (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    matches = re.findall(pattern, ifconfig_output, re.DOTALL)

    for match in matches:
        interface, ip, netmask = match
        print(f'{interface}: {ip}, mask = {netmask}')

parse_ifconfig()
