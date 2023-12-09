import config
from socket import*
import re

# POP3 server settings
host = config.mailServer
port = config.pop3 
username = "kakaka@gmail.com"
password = config.password
pop3_socket = socket(AF_INET, SOCK_STREAM)  
pop3_socket.connect((host,port))
response = pop3_socket.recv(1024).decode('utf-8')
def getMail(username,password=config.password) :
    user_command = f"USER {username}\r\n"
    pop3_socket.sendall(user_command.encode('utf-8'))
    response = pop3_socket.recv(1024).decode('utf-8')
    print(response)
    pass_command = f"PASS {password}\r\n"
    pop3_socket.sendall(pass_command.encode('utf-8'))
    response = pop3_socket.recv(1024).decode('utf-8')
    print(response)
    stat_command = "STAT\r\n"
    pop3_socket.sendall(stat_command.encode('utf-8'))
    response = pop3_socket.recv(2048).decode('utf-8')
    print(response)
    if response.startswith('+OK'):
        print(response)
        num_messages = int(response.split()[1])
        print(f"You have {num_messages} in your mailbox\n")
        if num_messages > 0:
            for message_number in range(1, num_messages + 1):
                retr_command = f"RETR {message_number}\r\n"
                pop3_socket.sendall(retr_command.encode('utf-8'))
                retr_response = pop3_socket.recv(4096).decode('utf-8')
                pattern = re.compile(r"From: (.+?)\nTo: (.+?)\nCc: (.+?)(?:\nBcc: (.+?))?\nSubject: (.+?)\n(.+)", re.DOTALL)
                match = pattern.search(retr_response)
                if match :
                    sender = match.group(1).strip()
                    to_addresses = match.group(2).strip()
                    cc_addresses = match.group(3).strip()
                    bcc_addresses = match.group(4).strip() if match.group(4) else ""
                    subject = match.group(5).strip()
                    body = match.group(6).strip()
                    # In ra cùng một dòng
                    print(f"{message_number}. {sender}, {subject}")



def quit():
    quit_command = "QUIT\r\n"
    pop3_socket.sendall(quit_command.encode('utf-8'))
    pop3_socket.recv(1024).decode('utf-8')
