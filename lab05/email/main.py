import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.message

def send_html_email(receiver_address, subject, content, sender_address, sender_pass):
    print('receiver = ', receiver_address)
    print('subject =', subject)
    print('content = ', content)
    print('sender_address = ', sender_address)
    print('sender_pass = ', sender_pass)
    message = email.message.EmailMessage()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject
    message.add_alternative(content, "html")

    session = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    session.ehlo()
    session.login(sender_address, sender_pass)
    session.send_message(message)
    session.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send an email.')
    parser.add_argument('--receiver', required=True, help='Receiver email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--content', required=True, help='Email content in HTML format')
    parser.add_argument('--sender', required=True, help='Sender email address')
    parser.add_argument('--password', required=True, help='Sender email password')

    args = parser.parse_args()

    send_html_email(args.receiver, args.subject, args.content, args.sender, args.password)
