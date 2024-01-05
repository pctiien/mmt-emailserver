from socket import *
import config
import os

import mimetypes
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

host=config.mailServer
smtpport=config.smtp
bufferSize = 2048


def recv_msg(client_socket):
  try:
    return client_socket.recv(bufferSize).decode()
  except timeout:
    return None


def send_msg(socket, message):
  socket.sendall(f"{message}\r\n".encode())
  recv = socket.recv(1024).decode()
  return recv


# gui file
def send_file(subject, body, from_addr, toEmail, ccEmail, bccEmail, attachment_paths):
    client_socket = socket(AF_INET, SOCK_STREAM)  # Tạo 1 socket
    client_socket.connect((host,smtpport))#Phải có
    client_socket.recv(1024)
    client_socket.sendall(f"EHLO\r\n".encode())
    client_socket.recv(1024)
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = ",".join(toEmail) #Do là một mảng
    msg["Subject"] = subject

    if len(ccEmail[0]) > 0:
        msg["Cc"] = ",".join(ccEmail)

    body_text = MIMEText(body)
    body_text.set_charset('UTF-8')
    body_text.set_param('format', 'flowed')
    msg.attach(body_text)
    if attachment_paths:
        for attachment_path in attachment_paths:
              
            file_size = get_file_size(attachment_path)

            # kiem tra kich thuoc file
            if file_size > 3 * 1024 * 1024:  
                print(f"File {os.path.basename(attachment_path)} khong gui duoc do co kich thuoc lon hon 3MB")
                continue 
              
            mime_type, _ = mimetypes.guess_type(attachment_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            
            main_type, sub_type = mime_type.split('/', 1)
            attachment = MIMEBase(main_type, sub_type)
            
            with open(attachment_path, 'rb') as attachment_file:
                attachment.set_payload(attachment_file.read())
                
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment;'
                                    f' filename="{os.path.basename(attachment_path)}"')#Thêm tên cho file cần gửi
            msg.attach(attachment)

    client_socket.sendall(f"MAIL FROM:<{from_addr}>\r\n".encode())
    client_socket.recv(1024)
    for mail in toEmail + ccEmail + bccEmail:
         client_socket.sendall(f"RCPT TO:<{mail}>\r\n".encode())
         client_socket.recv(1024)

    client_socket.sendall(f"DATA\r\n".encode())
    client_socket.recv(1024)
    client_socket.sendall(msg.as_bytes())
    client_socket.sendall(f"\r\n.\r\n".encode())
    reply=client_socket.recv(1024).decode()
    if reply.startswith("250"):
        print("Send successfully!")
    else:
        print("Error in sending the mail.")
    client_socket.sendall("QUIT\r\n".encode())
    client_socket.close()#Phải có
    
# tinh dung luong file
def get_file_size(file_path):
    return os.path.getsize(file_path)

# mang duong dan
def input_attachment_paths(num_paths):
  attachment_paths = []
  for i in range(num_paths):
    path = input(f"Nhap duong dan thu {i+1}: ")
    attachment_paths.append(path)
  return attachment_paths


