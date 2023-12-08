from socket import *
import config

bufferSize = 2048
client_socket = socket(AF_INET, SOCK_STREAM)  
client_socket.settimeout(5)
client_socket.connect((config.mailServer, config.smtp))

def recv_msg():
  try:
    return client_socket.recv(bufferSize).decode()
  except timeout:
    pass

def send_msg(message, expect_return_msg=True):
  client_socket.send(f"{message}\r\n".encode())
  if expect_return_msg:
    recv = recv_msg()
    print(recv)
    return recv

def ehlo():
    send_msg("EHLO",False)

def quit():
  return send_msg("QUIT",False)

def send_mail(subject,msg, from_addr, to_addr):
  for mail in to_addr: 
    ehlo()
    send_msg(f"MAIL FROM:<{from_addr}>")
    send_msg(f"RCPT TO:<{to_addr}>")
    send_msg(f"DATA")
    send_msg(f"Subject: {subject}\r\n", expect_return_msg=False)
    send_msg(msg, expect_return_msg=False)
    send_msg(".")
