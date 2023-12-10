from socket import *
import config
import os

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
  return send_msg("QUIT",True)

def connect():
  client_socket.connect((config.mailServer, config.smtp))
  ehlo()
def send_mail(subject,body, from_addr, toEmail,ccEmail,bccEmail):
  email_header = f"From: {from_addr}\r\n"
  email_header += f"To: {",".join(toEmail)}\r\n"
  if len(ccEmail)>0:
    email_header += f"Cc: {",".join(ccEmail)}\r\n"
  if len(bccEmail)>0 :
    print("kakakakaa")
    email_header += f"Bcc: {",".join(bccEmail)}"
  send_msg(f"MAIL FROM:<{from_addr}>")
  if len(toEmail+ccEmail)>0 :
    for mail in toEmail + ccEmail : 
      send_msg(f"RCPT TO:<{mail}>")
    send_msg(f"DATA")
    send_msg(f"{email_header}", expect_return_msg=False)
    send_msg(f"Subject: {subject}\r\n{body}\r\n.", expect_return_msg=False)
  # if len(bccEmail)>0 :
  #   for mail in bccEmail: 
  #     header  = email_header + f"Bcc: {mail}\r\n"
  #     ehlo()
  #     send_msg(f"RCPT TO:<{mail}>")
  #     send_msg(f"DATA")
  #     send_msg(f"Subject: {subject}\r\n", expect_return_msg=False)
  #     send_msg(f"{header}\r\n{body}\r\n.", expect_return_msg=False)

def create_folder(folder_name):
  try:
    os.makedirs(folder_name)
  except OSError as e:
    print(f"Error creating folder: {e}")
    return False
connect()
