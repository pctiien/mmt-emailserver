import sendmail as sending
import getmail as getting
import config

choice = '0'
while(choice != '3'):
    print("1.Send email")
    print("2.Get email")
    print("3.Exit")
    choice = input("Enter your choice : ")
    print(choice)
    if(choice =='3'): 
        sending.quit()
        getting.quit()
        break
    elif(choice == '1'):
        toEmail = input("To :")
        ccEmail = input("CC :")
        bccEmail = input("BCC :")
        toEmail = [email.strip() for email in toEmail.split(',')]
        ccEmail = [email.strip() for email in ccEmail.split(',')]
        bccEmail = [email.strip() for email in bccEmail.split(',')]
        email_subject = input("Subject :")
        email_msg = input("Content :")
        
        fileEmail = input("Co gui kem file(1.co, 2.khong): ")
        if(fileEmail == '1'):
            slFile = int(input("So luong file muon gui: "))
            for i in range(1,slFile+1):
                b = input(f"Cho biet duong dan thu {i} ")
            sending.send_file(subject=email_subject,body=email_msg,from_addr=config.username,toEmail=toEmail,ccEmail=ccEmail,bccEmail=bccEmail,attachment_path=b)
        elif(fileEmail == '2'):
            sending.send_mail(subject=email_subject,body=email_msg,from_addr=config.username,toEmail=toEmail,ccEmail=ccEmail,bccEmail=bccEmail)
            
    elif(choice == '2'):
        email_view = input("Email view :")
        if email_view =="":
            email_view = config.username
        getting.login(username=email_view)
        getting.getMail(username=email_view)

