from socket import *
import config
import base64

bufferSize = 2048
client_socket = socket(AF_INET, SOCK_STREAM)  

def recv_msg():
    try:
        return client_socket.recv(bufferSize).decode()
    except timeout:
        return None  

def send_msg(message, expect_return_msg=True):
    client_socket.send(f"{message}\r\n".encode())
    recv = recv_msg()
    if expect_return_msg:
        print(recv)
    return recv

def ehlo():
    send_msg("EHLO", False)

def quit():
    return send_msg("QUIT", True)

def connect():
    client_socket.connect((config.mailServer, config.smtp))
    ehlo()

def send_txt_mail(subject, body, from_addr, toEmail, ccEmail, bccEmail, file_path):
    # Đọc nội dung file txt
    with open(file_path, "r") as file:
        file_content = file.read()

    email_header = f"From: {from_addr}\r\n"
    email_header += f"To: {','.join(toEmail)}\r\n"
    if len(ccEmail) > 0:
        email_header += f"Cc: {','.join(ccEmail)}\r\n"

    if len(bccEmail) > 0:
        email_header += f"Bcc: {','.join(bccEmail)}\r\n"

    send_msg(f"MAIL FROM:<{from_addr}>")
    
    if len(toEmail + ccEmail) > 0:
        for mail in toEmail + ccEmail:
            send_msg(f"RCPT TO:<{mail}>")

        send_msg("DATA")
        send_msg(f"{email_header}\r\nSubject: {subject}\r\n{body}\r\n{file_content}\r\n.", expect_return_msg=False)

# Gửi email với file txt đính kèm
connect()
send_txt_mail("Test Subject", "Test Body", "sender@example.com", ["recipient@example.com"], ["cc@example.com"], ["bcc@example.com"], "path/to/your/file.txt")

# Đóng kết nối
quit()