import config
from socket import *
import os
import select
import json
import loc

# POP3 server settings
host = config.mailServer
port = config.pop3
username = config.username
password = config.password


def login(pop3_socket,username=config.username, password=config.password):
    user_command = f"USER {username}\r\n"
    pop3_socket.sendall(user_command.encode('utf-8'))
    pop3_socket.recv(1024)
    pass_command = f"PASS {password}\r\n"
    pop3_socket.sendall(pass_command.encode('utf-8'))
    pop3_socket.recv(1024)

maxsize = 1024

def search(string,dest):
    for j in dest:
        if string==j:
            return True
    return False
def recvall(pop3_socket,size=maxsize):
    fragments = []
    while True:
        chunk = pop3_socket.recv(size).decode()
        if not chunk:  # Cài đặt cho lần nhận đầu tiên không có data nào sẽ thoát
            break
        fragments.append(chunk)
        readable, writable, exceptional = select.select([pop3_socket], [], [], 0)
        if not readable:
            break
    message = "".join(fragments)
    return message
def getMail(username=config.username, password=config.password):
    pop3_socket = socket(AF_INET, SOCK_STREAM)
    pop3_socket.connect((host, port))
    pop3_socket.recv(maxsize)
    login(pop3_socket)
    stat_command = "STAT\r\n"
    pop3_socket.sendall(stat_command.encode('utf-8'))
    response = recvall(pop3_socket)
    if response.startswith('+OK'):
        num_messages = int(response.split()[1])  # so luong thu trong mailbox
        uidl_command = "UIDL\r\n"  # Xac dinh id cua moi thu
        pop3_socket.sendall(uidl_command.encode('utf-8'))
        response = recvall(pop3_socket)
        uidList = response.split('\r\n')[1:]  # tách các dòng và bỏ dòng phản hồi trạng thái
        uidArrayDict=[]
        for i in range(num_messages):
            uidDictionary={}
            temp=uidList[i].split()
            uidDictionary["message_number"]=temp[0]
            uid=temp[1]
            uid=uid.split('.')[0]
            uidDictionary["UID"]=uid
            uidArrayDict.append(uidDictionary)
        if not os.path.exists("UIDstore.json"):
            containedUIDs=[]
        else:
            with open("UIDstore.json","r") as fp:
                containedUIDs=json.load(fp)#Mở 1
        for item in uidArrayDict:
            if not search(item["UID"],containedUIDs):
                tempdict={}
                containedUIDs.append(item["UID"])
                command="RETR {}{}".format(item['message_number'],"\r\n")
                pop3_socket.sendall(command.encode())
                message=recvall(pop3_socket)
                message=message.split('\r\n',1)[1]#Tách dòng phản hồi trạng thái
                folder,sender,subject,text,attachment=loc.locthu(message)
                #Thêm phần dictionary dùng cho việc in danh sách thư
                tempdict['state']=0
                tempdict['sender']=sender
                tempdict['subject']=subject
                tempdict['name']=item["UID"]
                #===========================
                #Thêm phần dictionary vào file quản lí
                path=os.getcwd()
                managefile=os.path.join(path,"Home",folder,'quanly.json')
                TatCaThu=[]
                if not os.path.exists(managefile):
                    with open(managefile,'wt') as mf:
                        json.dump([],mf)
                if os.path.exists(managefile):
                    fp=open(managefile,'rt')#Mở 2
                    TatCaThu=json.load(fp)
                    fp.close()
                TatCaThu.append(tempdict)
                with open(managefile,'wt') as fp:
                    json.dump(TatCaThu,fp)#Đã đóng 2
                #===========================
                #Xử lí phần text và attachment
                emailfile=os.path.join(path,"Home",folder,tempdict["name"])
                email_text_file=os.path.join(emailfile,"text_file.txt")
                if not os.path.exists(emailfile):
                    os.makedirs(emailfile)
                fp=open(email_text_file,"wt",newline='')#Lưu file text chứa nội dung thư
                fp.write(text)
                fp.close()
                if attachment:
                    email_attach_file=os.path.join(emailfile,"attach")
                    if not os.path.exists(email_attach_file):
                        os.makedirs(email_attach_file)
                    for i in attachment:
                        filepath=os.path.join(email_attach_file,i[0])
                        fp=open(filepath,"wb")#i[0] chính là tên file attach
                        fp.write(i[1])
                        fp.close()
        #========================
        fp=open("UIDstore.json",'wt')
        json.dump(containedUIDs,fp)#Đóng 1
        fp.close()
    pop3_socket.sendall(b"QUIT\r\n")
    pop3_socket.close()

def deleteMail(pop3_socket):
    pop3_socket.send(f"DELE {1}\r\n".encode())
    response = recvall(pop3_socket)
    print(response)




