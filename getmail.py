import config
from socket import*
import re
import tkinter as tk
from tkinter import filedialog
import easygui

# POP3 server settings
host = config.mailServer
port = config.pop3 
username = "kakaka@gmail.com"
password = config.password
pop3_socket = socket(AF_INET, SOCK_STREAM)  
pop3_socket.connect((host,port))
response = pop3_socket.recv(1024).decode('utf-8')
def login(username=config.username,password=config.password):
    user_command = f"USER {username}\r\n"
    pop3_socket.sendall(user_command.encode('utf-8'))
    response = pop3_socket.recv(1024).decode('utf-8')
    print(response)
    pass_command = f"PASS {password}\r\n"
    pop3_socket.sendall(pass_command.encode('utf-8'))
    response = pop3_socket.recv(1024).decode('utf-8')
    print(response)
def getMail(username,password=config.password) :
    stat_command = "STAT\r\n"
    pop3_socket.sendall(stat_command.encode('utf-8'))
    response = pop3_socket.recv(2048).decode('utf-8')
    print(response)
    if response.startswith('+OK'):
        print(response)
        num_messages = int(response.split()[1])
        print(f"You have {num_messages} in your mailbox\n")
        if num_messages > 0:
            list_msg = []
            list_sender =[]
            list_subject =[]
            for message_number in range(1, num_messages + 1):
                retr_command = f"RETR {message_number}\r\n"
                pop3_socket.sendall(retr_command.encode('utf-8'))
                retr_response = pop3_socket.recv(4096).decode('utf-8')
                retr_response = '\n'.join(retr_response.splitlines()[1:])
                pattern = re.compile(r"From: (.+?)\nTo: (.+?)\nCc: (.+?)(?:\nBcc: (.+?))?\nSubject: (.+?)\n(.+)", re.DOTALL)
                match = pattern.search(retr_response)
                list_msg.append(retr_response)  
                if match :
                    sender = match.group(1).strip()
                    to_addresses = match.group(2).strip()
                    cc_addresses = match.group(3).strip()
                    bcc_addresses = match.group(4).strip() if match.group(4) else ""
                    subject = match.group(5).strip()
                    body = match.group(6).strip()
                    # In ra cùng một dòng
                    list_sender.append(sender)
                    list_subject.append(subject)
                    print(f"{message_number}. {sender}, {subject}")
            choice ='0'
            while True:
                choice = input("your email number: (enter = exit, 0 = list) ")
                if(choice=='0'):
                    print("size:",len(list_sender))
                    for i in range(0,len(list_sender)):
                        print(f"{i+1}. {list_sender[i]}, {list_subject[i]}")
                elif(choice==''): break;
                elif int(choice) > len(list_msg) :
                    break;
                else : 
                    email_content = list_msg[int(choice)-1]
                    print(email_content)
                    download_choice = input("do you want to download this file ?(0=no, 1=yes)")
                    if(download_choice == '1'):
                        downloadMail(email_content,choice)

def downloadMail(email_content,email_number,path=""):
    path = input("Enter the path to save email (enter for default): ")
    if path=="":
        path = f"email_{email_number}.txt"
    with open(path, "w", encoding="utf-8") as file:
        file.write(email_content)
def deleteMail():
    pop3_socket.send(f"DELE {1}\r\n".encode())
    response = pop3_socket.recv(1024).decode()
    print(response)
def quit():
    quit_command = "QUIT\r\n"
    pop3_socket.sendall(quit_command.encode('utf-8'))
    pop3_socket.recv(1024).decode('utf-8')
