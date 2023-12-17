from socket import *
import config
import os
from tkinter import *

import mimetypes
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


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
    send_msg("EHLO",False)
    
def quit():
  return send_msg("QUIT",False)

def connect():
  client_socket.connect((config.mailServer, config.smtp))
  ehlo()
  
def send_mail(subject, body, from_addr, toEmail,ccEmail,bccEmail):
  email_header = f"From: {from_addr}\r\n"
  email_header += f"To: {",".join(toEmail)}\r\n"
  
  if len(ccEmail)>0:
    email_header += f"Cc: {",".join(ccEmail)}\r\n"
 
  if len(bccEmail)>0 :
    email_header += f"Bcc: {",".join(bccEmail)}\r\n"
  email_header +=f"Subject: {subject}\r\n"
  send_msg(f"MAIL FROM:<{from_addr}>")

  for mail in toEmail + ccEmail + bccEmail:
    send_msg(f"RCPT TO:<{mail}>")
  send_msg(f"DATA")
  send_msg(f"{email_header}", expect_return_msg=False)
  send_msg(f"{body}\r\n.", expect_return_msg=False)

# gui file
def send_file(subject, body, from_addr, toEmail, ccEmail, bccEmail, attachment_paths=None):
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = ",".join(toEmail)
    msg["Subject"] = subject

    if len(ccEmail) > 0:
        msg["Cc"] = ",".join(ccEmail)

    if len(bccEmail) > 0:
        print("kakakakaa")
        msg["Bcc"] = ",".join(bccEmail)
    
    body_text = MIMEText(body)
    body_text.set_charset('UTF-8')
    body_text.set_param('format', 'flowed') 
    msg.attach(body_text)
    

        
    if attachment_paths:
        #msg.attach(MIMEText(body, 'plain',"UTF-8"))
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
            attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
            msg.attach(attachment)

    send_msg(f"MAIL FROM:<{from_addr}>\r\n")

    if len(toEmail + ccEmail) > 0:
        for mail in toEmail + ccEmail:
            send_msg(f"RCPT TO:<{mail}>")

    send_msg("DATA")
    send_msg(msg.as_string(), expect_return_msg=False)
    send_msg(".", expect_return_msg=False)
    
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
  
connect()

