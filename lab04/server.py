import json
import socket
import requests
import sys
import os
import logging
import shutil
    
blacklist = list()
cache_metadata = {}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('log.txt')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
def log(message):
    logger.info(message)
    print(message)

def ok_response(content):
    return bytes(f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}', 'utf-8')

def get_url(request):
    lines = request.split('\n')
    for line in lines:
        if line.startswith('GET'):
            parts = line.split(' ')
            if len(parts) > 1:
                return parts[1][1:]
    return None

def get_request(client_connection):
    request = []
    while True:
        data = client_connection.recv(4096)
        request.extend(data)
        if len(data) < 4096:
            break
    return bytes(request).decode('utf-8')

def get_filename(url):
    return f'tmp_cache/{url.replace("/", ".")}'

def write_to_cache(response, url):
    if response.status_code == 200:
        cache_metadata[url] = {'last_modified': response.headers.get('Last-Modified'), 'etag': response.headers.get('ETag')}
        content = response.content.decode()
        with open(get_filename(url), 'w') as file:
            file.write(content)

if __name__ == "__main__":
    if (len(sys.argv[1:]) != 1):
        log(f"python3 server.py port")
        sys.exit(1)

    port = int(sys.argv[1])
    log(f"running on localhost:{port}")
    with open('blacklist.txt', 'r') as file:
        blacklist = [line.strip() for line in file]

    if not os.path.exists('tmp_cache/'):
        os.mkdir('tmp_cache/')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)

    while True:
        client_socket, _ = server_socket.accept()
        request = get_request(client_socket)
        try:
            method = request.split()[0]
            url = get_url(request)
            log(f"{method} request: {url}")
            if url in blacklist:
                log(f"{url} is blacklisted")
                client_socket.sendall(ok_response('Requested URL is blacklisted'))
                client_socket.close()
                continue
            if method == 'GET':
                if url in cache_metadata:
                    last_modified = cache_metadata.get(url, {}).get('last_modified')
                    etag = cache_metadata.get(url, {}).get('etag')
                    headers = {'If-Modified-Since': last_modified, 'If-None-Match': etag}
                    response = requests.get(url, headers=headers)
                    if response.status_code == 304:
                        log(f"GET: {url} getting from cache")
                        with open(get_filename(url), 'r') as file:
                            content = file.read()
                            client_socket.sendall(ok_response(content))
                        client_socket.close()   
                        continue
                    else:
                        write_to_cache(response, url)
                else:
                    response = requests.get(url)
                    write_to_cache(response, url)
            elif method == 'POST':
                data = request.split('\r\n\r\n', 1)[1]
                log(f"POST data: {data}")
                response = requests.post(url, data=data)
            log(f"Response code {url}: {response.status_code}")
            if (response.status_code == 404):
                client_socket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
            else:
                client_socket.sendall(ok_response(response.content.decode()))
            client_socket.close()
        except Exception as e:
            log(f"Error: {e}")
            client_socket.sendall(b'HTTP/1.1 400 Bad Request\r\n\r\n')
            client_socket.close()
            continue
    server_socket.close()
