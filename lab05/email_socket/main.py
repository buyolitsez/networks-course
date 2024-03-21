import argparse
import socket
import base64

CRLF = "\r\n"
END_OF_MESSAGE = "\r\n.\r\n"

def send_email_via_socket(smtp_server, smtp_port, sender_address, sender_pass, receiver_address, subject, content):
    print('receiver = ', receiver_address)
    print('subject =', subject)
    print('content = ', content)
    print('sender_address = ', sender_address)
    print('sender_pass = ', sender_pass)

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    with socket.create_connection((smtp_server, smtp_port)) as server_socket:
        # server_socket.connect((smtp_server, smtp_port))
        recv = server_socket.recv(1024).decode()

        ehlo_command = f'EHLO cool.hacker.server{CRLF}'
        server_socket.send(ehlo_command.encode())
        recv = server_socket.recv(1024).decode()
        print(recv)

        auth_login_command = f'AUTH LOGIN{CRLF}'
        server_socket.send(auth_login_command.encode())
        recv = server_socket.recv(1024).decode()
        print(recv)

        username = base64.b64encode(sender_address.encode())
        server_socket.send(username + CRLF.encode())
        recv = server_socket.recv(1024).decode()
        print(recv)

        password = base64.b64encode(sender_pass.encode())
        server_socket.send(password + CRLF.encode())
        recv = server_socket.recv(1024).decode()
        print(recv)

        mail_from_command = f'MAIL FROM:<{sender_address}>{CRLF}'
        server_socket.send(mail_from_command.encode())
        recv = server_socket.recv(1024).decode()
        print(recv)

        rcpt_to_command = f'RCPT TO:<{receiver_address}>{CRLF}'
        server_socket.send(rcpt_to_command.encode())
        recv = server_socket.recv(1024).decode()
        print(recv)

        data_command = f'DATA{CRLF}'
        server_socket.send(data_command.encode())
        recv = server_socket.recv(1024).decode()
        print(recv)

        subject = f'Subject: {subject}{CRLF}'
        server_socket.send(subject.encode())

        to = f'To: {receiver_address}{CRLF}'
        server_socket.send(to.encode())

        from_ = f'From: {sender_address}{CRLF}'
        server_socket.send(from_.encode())

        server_socket.send(CRLF.encode())
        server_socket.send(content.encode())
        server_socket.send(END_OF_MESSAGE.encode())
        recv = server_socket.recv(1024).decode()
        print(recv)

        quit_command = f'QUIT{CRLF}'
        server_socket.send(quit_command.encode())
        recv = server_socket.recv(1024).decode()
        print(recv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send an email.')
    parser.add_argument('--receiver', required=True, help='Receiver email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--content', required=True, help='Email content in HTML format')
    parser.add_argument('--sender', required=True, help='Sender email address')
    parser.add_argument('--password', required=True, help='Sender email password')

    args = parser.parse_args()

    send_email_via_socket('smtp.yandex.ru', 465, args.sender, args.password, args.receiver, args.subject, args.content)
