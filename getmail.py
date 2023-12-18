import config
from socket import*
import re
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
    pass_command = f"PASS {password}\r\n"
    pop3_socket.sendall(pass_command.encode('utf-8'))
    response = pop3_socket.recv(1024).decode('utf-8')
def getMail(username=config.username,password=config.password) :
    stat_command = "STAT\r\n"
    pop3_socket.sendall(stat_command.encode('utf-8'))
    response = pop3_socket.recv(4096).decode('utf-8')
    if response.startswith('+OK'):
        num_messages = int(response.split()[1])
        uidl_command = "UIDL\r\n"
        pop3_socket.sendall(uidl_command.encode('utf-8'))
        response = pop3_socket.recv(4096).decode('utf-8')
        uidList = response.split('\r\n');
        uidList = [item.split()[1].split('.')[0] for item in uidList if len(item)>3] 
        if num_messages > 0:
            list_mail = []
            for i in range(0,len(uidList)):
                retr_command = f"RETR {i+1}\r\n"
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
                    mail = MailClient(sender,to_addresses,cc_addresses,bcc_addresses,subject,body,uidList[i])
                    mail.isRead = mail.checkRead()
                    list_mail.append(mail)
                    # In ra cùng một dòng
            print("these are list of folders in your mailbox :")
            print("1. Inbox\n2.Project\n3.Important\n4.Work\n5.Spam")
            choice ='0'
            choice = input("which folder do you want to read mail :")
            list_mailRead = []
            if choice =='1':
                list_mailRead =[mail for mail in list_mail if mail.getFolderType()=="Inbox"]
            elif choice =='2':
                list_mailRead =[mail for mail in list_mail if mail.getFolderType()=="Project"]
            elif choice =='3':
                list_mailRead =[mail for mail in list_mail if mail.getFolderType()=="Important"]
            elif choice =='4':
                list_mailRead =[mail for mail in list_mail if mail.getFolderType()=="Work"]
            elif choice =='5':
                list_mailRead =[mail for mail in list_mail if mail.getFolderType()=="Spam"]
            for i in range(0,len(list_mailRead)):
                list_mailRead[i].display_brief(i+1)
            choice = '0'
            if len(list_mailRead)>0 :
                while True:
                    choice = input("which email number you want to read: (enter = exit, 0 = list) ")
                    if(choice=='0'):
                        print("size:",len(list_mailRead))
                        for i in range(0,len(list_mailRead)):
                            list_mail[i].display_brief(i+1)
                    elif(choice==''): break;
                    elif int(choice) > len(list_mailRead) :
                        break;
                    else :
                        list_mailRead[int(choice)-1].isRead = True 
                        mailClient = list_mailRead[int(choice)-1]
                        folderType = mailClient.getFolderType()
                        create_folder(config.folderpath,username,folderType,mailClient.getStrInfo(),mailClient.uid)
                        mailClient.display_info()
            else: print("There is no mail")
        else : 
            print("There is no mail ")

# def downloadMail(mailContent,mailId,path=""):
#     path = input("Enter the path to save email (enter for default): ")
#     if path=="":
#         path = f"email_{mailId}.txt"
#     with open(path, "w", encoding="utf-8") as file:
#         file.write(mailContent)
#         file.close()

def downloadMail(mailContent, mailId, attachmentContents=None, attachmentNames=None, path=""):
    path = input("Enter the path to save email (enter for default): ")
    if path == "":
        path = f"email_{mailId}.txt"
    
    with open(path, "w", encoding="utf-8") as file:
        file.write(mailContent)

    if attachmentContents is not None and attachmentNames is not None:
        for attachmentContent, attachmentName in zip(attachmentContents, attachmentNames):
            save_attachment = input(f"This email has an attached file '{attachmentName}', do you want to save it locally? (yes/no): ")
            if save_attachment.lower() == 'yes':
                download_attachment(attachmentContent, attachmentName)
   
def download_attachment(attachmentContent, attachmentName):
    save_path = input("Enter the path to save the attachment (press Enter for default): ")
    if save_path == "":
        save_path = attachmentName

    with open(save_path, "w", encoding="utf-8") as attachment_file:
        attachment_file.write(attachmentContent)

def deleteMail():
    pop3_socket.send(f"DELE {1}\r\n".encode())
    response = pop3_socket.recv(1024).decode()
    print(response)
def quit():
    quit_command = "QUIT\r\n"
    pop3_socket.sendall(quit_command.encode('utf-8'))
    response = pop3_socket.recv(1024).decode('utf-8')
def create_folder(folderName,userName,folderType,mailContent,mailId):
  path = f"{folderName}/{userName}/{folderType}"
  try:
    if os.path.exists(path) == False :
        os.makedirs(path) 
    path += f"/{mailId}.txt"     
    with open(path, "w", encoding="utf-8") as file:
            file.write(mailContent)
            file.close()   
    return True;
  except OSError as e:
    print(f"Error creating folder: {e}")
    return False
