from socket import *
import config
import ssl
import base64

HOST = config.mailServer 
PORT = config.smtp        
SENDER = config.username
PASSWORD = base64.b64encode(config.password.encode()).decode()

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.settimeout(5)
client_socket.connect((HOST, PORT))
client_socket.send(b"HELO\r\n")
response = client_socket.recv(1024).decode()
print(response)
def send_msg(message):
    client_socket.send(message.encode())
    recv = client_socket.recv(1024)
    print(recv)
def create_auth_message(user: str, password: str):
    auth_str = "\x00" + user + "\x00" + password
    base64_str = base64.b64encode(auth_str.encode()).decode()
    return f"AUTH PLAIN {base64_str}\r\n"
def login(user, password):
    auth_msg = create_auth_message(user, password)
    send_msg(auth_msg)

login(SENDER,PASSWORD)