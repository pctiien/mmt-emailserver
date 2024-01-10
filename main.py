import json
import os
import shutil
import loc
import sendmail as sending
import config
import laythu
import threading
import time


time_autoload=config.autoload

def AutoLoad(timesleep):
    while flag == False:
        laythu.getMail()
        time.sleep(timesleep)

flag=False
autoload_thread=threading.Thread(target=AutoLoad,args=(time_autoload,))
autoload_thread.start()
def isEmptyFolder(path):
    return not os.listdir(path)
def move_folder(source_folder, destination_folder):
    if source_folder==destination_folder :
        return 
    try:
        shutil.move(source_folder, destination_folder)
    except Exception as e:
        print(f"Occur error when moving folder: {e}")     
def printMailList(mails):
    for i in range(len(mails)):
        state = ""
        if mails[i]["state"] == 0:  # Thư chưa được đọc
            state = "(Unread)"
        print(f"{i}. {state} From: {mails[i]["sender"]}, Subject: {mails[i]["subject"]}")

choice = '0'
while (choice != '3'):
    print("1.Send email")
    print("2.Get email")
    print("3.Exit")
    choice = input("Enter your choice: ")
    if (choice == '3'):
        flag=True
        print("Please wait for a moment...")
        autoload_thread.join()
        break
    elif (choice == '1'):
        print("Please enter information, if more than one element, separate by commas, press \"Enter\" to skip: ")
        toEmail = input("To :")
        while not toEmail:
            print("This is the required field, please enter again.")
            toEmail = input("To :")
        ccEmail = input("CC :")
        bccEmail = input("BCC :")
        toEmail = [email.strip() for email in toEmail.split(',')] #Tạo mảng
        ccEmail = [email.strip() for email in ccEmail.split(',')]
        bccEmail = [email.strip() for email in bccEmail.split(',')]
        email_subject = input("Subject: ")
        email_msg = input("Content: ")
        fileEmail = input("Attach file(1.yes, 2.no): ")
        attachment_paths = []
        if (fileEmail == '1'):
            print("File must be smaller than 3 MB")
            slFile = int(input("Number of files to send: "))
            attachment_paths = sending.input_attachment_paths(slFile)
        sending.send_file(subject=email_subject, body=email_msg, from_addr=config.username,
                          toEmail=toEmail, ccEmail=ccEmail, bccEmail=bccEmail,
                          attachment_paths=attachment_paths)
            
    elif (choice == '2'):
        laythu.getMail()
        FolderArray = loc.TakeFolderName()
        print("These are list of folders in your mailbox: ")
        for i in range(len(FolderArray)):
            print("%d. %s" % (i, FolderArray[i]))
        choice = 1
        while choice:
            #Vòng lặp cha
            in_put=input("Which folder do you want to read mail (press \"Enter\" to exit, enter \"list\" to see folders list again): ")
            if in_put == '':
                break
            if in_put == 'list':
                print("These are list of folders in your mailbox: ")
                for i in range(len(FolderArray)):
                    print("%d. %s" % (i, FolderArray[i]))
                continue
            in_put=int(in_put)
            if in_put <0 or in_put >=len(FolderArray):
                print("Unvalid input, please choose again.")
                continue
            path=os.getcwd()
            folder_path=os.path.join(path,"Home",FolderArray[in_put])
            if isEmptyFolder(folder_path):
                print("There are not any mails.")
                continue
            filename=os.path.join(folder_path,"quanly.json")
            fp=open(filename,'rt')
            mails=json.load(fp)
            fp.close()  #Mở 1, đợi đóng
            printMailList(mails)
            while True:
                # Vòng lặp thứ 2
                choice_mail = input("Which email number you want to read (press \"Enter\" to return Home folder, enter \"list\" to see mails list again): ")
                if choice_mail == '':
                    print("Returning to Home folder.")
                    break
                if choice_mail == "list":
                    fp = open(filename, 'rt')
                    mails = json.load(fp)
                    fp.close()  #Cập nhật lại email, có thể có thư mới
                    printMailList(mails)
                    continue
                else:
                    choice_mail = int(choice_mail)
                    if choice_mail <0 or choice_mail>= len(mails):
                        print("Unvalid input, please choose again.")
                        continue
                    fp=open(filename,'rt')#Cập nhật lại, có khả năng autoload đã cập nhật thư mới
                    mails=json.load(fp)
                    fp.close()
                    mails[choice_mail]["state"]=1 #Đánh dấu đã đọc
                    fp=open(filename,'wt')
                    json.dump(mails,fp)
                    fp.close() # Đã đóng 1
                    emailfolder=os.path.join(folder_path,mails[choice_mail]["name"])
                    mail_text_path=os.path.join(emailfolder,"text_file.txt")
                    mail_attatch_path=os.path.join(emailfolder,"attach")
                    print(f"This is the mail number {choice_mail}: ")
                    fp=open(mail_text_path,'rt')
                    print(fp.read())
                    fp.close()
                    print(f"Mark as spam email (Please enter \"yes\" or \"no\")?")#Sửa lại cho đồng bộ
                    input_choose = input()
                    if input_choose =='yes':
                        workingPath=os.getcwd()
                        spamFolderPath=os.path.join(workingPath,"Home","Spam")#Thư mục Spam có thể có số thứ tự khác nhau, gán tên cụ thể
                        curFolderPath = emailfolder#tên thư mục hiện tại
                        jsonSpamFile = os.path.join(spamFolderPath,'quanly.json')#file quản lí của Spam
                        spamMails = []
                        if(spamFolderPath != folder_path) :
                            if os.path.exists(jsonSpamFile):#Khi tồn tại thì đọc, không vẫn là mảng rỗng
                                with open(jsonSpamFile,'rt') as spam:
                                    spamMails = json.load(spam)
                            spamMails.append(mails[choice_mail]) #Không cần cập nhật mails
                            with open(jsonSpamFile,'wt') as spam:
                                json.dump(spamMails,spam)
                            
                            move_folder(curFolderPath,spamFolderPath)
                            fp = open(filename, 'rt')  # Cập nhật lại mails, có khả năng autoload đã cập nhật thư mới
                            mails = json.load(fp)
                            fp.close()
                            del mails[choice_mail]
                            if mails==[]:
                                os.remove(filename) #Nếu đã không còn thư, xóa luôn file quanly.json
                            else:
                                with open(filename,'wt') as curMailFile:
                                    json.dump(mails,curMailFile)
                            print("This mail has been sent to spam folder")
                        else :
                            print("Both folders are already in the same directory")
                    else:
                        if os.path.exists(mail_attatch_path):
                            attachments=os.listdir(mail_attatch_path)
                            n=len(attachments)
                            if n>1:
                                print(f"There are {n} attached files: ")
                            if n==1:
                                print("There is 1 attach file: ")
                            for i in range(n):
                                print(f"Name of the file number {i}: {attachments[i]}")
                            for i in range(n):
                                in_put=input(f"Do you want to save file \"{attachments[i]}\" (Please enter \"yes\" or \"no\")? ")
                                if in_put=="yes":
                                    input_direction=input("Please enter the path which will save file: ")
                                    while not os.path.isdir(input_direction):
                                        input_direction=input("Unvalid path or path does not exist, please enter again, press \"Enter\" to exit: ")
                                        if input_direction=='':
                                            break
                                    if input_direction:
                                        local_file_name=os.path.join(input_direction,attachments[i])
                                        if os.path.exists(local_file_name):
                                            solve_same_name=input("File existed, do you want to overwrite (enter 1) or change file name (enter 2)? (press \"Enter\" to exit)")
                                            if solve_same_name == 1 or solve_same_name == 2:
                                                if solve_same_name == 2:  # nếu là 2 thì đổi tên, một giữ nguyên tên
                                                    new_name = input("Enter the new name (include file name extension): ")
                                                    local_file_name = os.path.join(input_direction, new_name)
                                            else:
                                                continue
                                                # Không cần ghi thêm nữa
                                        source = os.path.join(mail_attatch_path, attachments[i])
                                        shutil.copy(source, local_file_name)
                                        print("Save successfully!")

