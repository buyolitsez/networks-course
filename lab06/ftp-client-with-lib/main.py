import argparse
from ftplib import FTP

def connect_ftp(server, username, password):
    ftp = FTP(server)
    ftp.login(user=username, passwd=password)
    return ftp

def list_files(ftp):
    ftp.retrlines('LIST')

def upload_file(ftp, filename):
    with open(filename, 'rb') as file:
        ftp.storbinary('STOR ' + filename, file)

def download_file(ftp, filename):
    with open(filename, 'wb') as file:
        ftp.retrbinary('RETR ' + filename, file.write)

def main():
    parser = argparse.ArgumentParser(description='FTP client')
    parser.add_argument('--server', type=str, required=True)
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    args = parser.parse_args()

    ftp = connect_ftp(args.server, args.username, args.password)

    print("Файлы на сервере")
    list_files(ftp)

    print('Загружаем файл send.txt')
    upload_file(ftp, 'send.txt')

    print('Скачиваем файл format.sh')
    download_file(ftp, 'format.sh')

    ftp.quit()

if __name__ == "__main__":
    main()
