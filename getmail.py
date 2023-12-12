import config
from socket import*
import re
import tkinter as tk
from tkinter import filedialog
import os
from MailClient import MailClient

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
def getMail(username=config.username,password=config.password) :
    stat_command = "STAT\r\n"
    pop3_socket.sendall(stat_command.encode('utf-8'))
    response = pop3_socket.recv(2048).decode('utf-8')
    print(response)
    if response.startswith('+OK'):
        print(response)
        num_messages = int(response.split()[1])
        print(f"You have {num_messages} in your mailbox\n")
        if num_messages > 0:
            list_mail = []
            for message_number in range(0, num_messages):
                retr_command = f"RETR {message_number+1}\r\n"
                pop3_socket.sendall(retr_command.encode('utf-8'))
                retr_response = pop3_socket.recv(4096).decode('utf-8')
                retr_response = '\n'.join(retr_response.splitlines()[1:])
                pattern = re.compile(r"From: (.+?)\nTo: (.+?)\nCc: (.+?)(?:\nBcc: (.+?))?\nSubject: (.+?)\n(.+)", re.DOTALL)
                match = pattern.search(retr_response)
                if match :
                    sender = match.group(1).strip() 
                    to_addresses = [match.group(2).strip()]
                    cc_addresses = [match.group(3).strip()]
                    bcc_addresses = [match.group(4).strip()] if match.group(4) else []
                    subject = match.group(5).strip()
                    body = match.group(6).strip()
                    list_mail.append(MailClient(sender,to_addresses,cc_addresses,bcc_addresses,subject,body))
                    list_mail[message_number].isRead = list_mail[message_number].checkRead(message_number+1,username)
                    # In ra cùng một dòng
                    list_mail[message_number].display_brief(message_number+1)
            choice ='0'
            while True:
                choice = input("which email number you want to read: (enter = exit, 0 = list) ")
                if(choice=='0'):
                    print("size:",len(list_mail))
                    for i in range(0,len(list_mail)):
                        list_mail[i].display_brief(i+1)
                elif(choice==''): break;
                elif int(choice) > len(list_mail) :
                    break;
                else : 
                    mailClient = list_mail[int(choice)-1]
                    folderType = mailClient.getFolderType()
                    create_folder(config.folderpath,username,folderType,mailClient.getStrInfo(),int(choice))
                    mailClient.display_info()
                    download_choice = input("do you want to download this file ?(0=no, 1=yes)")
                    if(download_choice == '1'):
                        downloadMail(list_mail[int(choice)-1].getStrInfo(),choice)

def downloadMail(mailContent,mailId,path=""):
    path = input("Enter the path to save email (enter for default): ")
    if path=="":
        path = f"email_{mailId}.txt"
    with open(path, "w", encoding="utf-8") as file:
        file.write(mailContent)
        file.close()
def deleteMail():
    pop3_socket.send(f"DELE {1}\r\n".encode())
    response = pop3_socket.recv(1024).decode()
    print(response)
def quit():
    quit_command = "QUIT\r\n"
    pop3_socket.sendall(quit_command.encode('utf-8'))
    pop3_socket.recv(1024).decode('utf-8')
def create_folder(folderName,userName,folderType,mailContent,mailId):
  path = f"{folderName}/{userName}/{folderType}"
  try:
    if os.path.exists(path) == False :
        os.makedirs(path) 
    path += f"/email_{mailId}.txt"     
    with open(path, "w", encoding="utf-8") as file:
            file.write(mailContent)
            file.close()   
    return True;
  except OSError as e:
    print(f"Error creating folder: {e}")
    return False