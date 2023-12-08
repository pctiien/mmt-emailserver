from socket import *
import ssl
import base64
import config

bufferSize = 2048

def create_auth_message(user: str, password: str):
  str = "\x00"+user+"\x00"+password
  base64_str = base64.b64encode(str.encode())
  return "AUTH PLAIN " + base64_str.decode()

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
    send_msg("EHLO")

def quit():
  return send_msg("QUIT")

def send_mail(msg, from_addr, to_addr):
  send_msg(f"MAIL FROM:<{from_addr}>")
  send_msg(f"RCPT TO:<{to_addr}>")
  send_msg(f"DATA")
  send_msg(f"SUBJECT: Hye! Maheen here\r\n", expect_return_msg=False)
  send_msg(msg, expect_return_msg=False)
  send_msg(".")

ehlo()
send_mail("I am PCTIEN;) I am studing US.",
          "maheenamin9@gmail.com", "kakaka@gmail.com")
quit()