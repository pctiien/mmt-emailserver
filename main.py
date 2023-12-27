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
        print("Please enter information, if more than one element, separate by commas, press \"Enter\" to skip: ")
        toEmail = input("To :")
        while not toEmail:
            print("This is the required field, please enter again.")
            toEmail = input("To :")
        ccEmail = input("CC :")
        bccEmail = input("BCC :")
        toEmail = [email.strip() for email in toEmail.split(',')]
        ccEmail = [email.strip() for email in ccEmail.split(',')]
        bccEmail = [email.strip() for email in bccEmail.split(',')]
        email_subject = input("Subject :")
        email_msg = input("Content :")
        fileEmail = input("Co gui kem file(1.co, 2.khong): ")
        attachment_paths = []
        if(fileEmail == '1'):
            print("File duoc gui phai co kich thuoc nho hon 3MB")
            slFile = int(input("So luong file muon gui: "))
            attachment_paths = sending.input_attachment_paths(slFile)
        sending.send_file(subject=email_subject, body=email_msg, from_addr=config.username,
                          toEmail=toEmail, ccEmail=ccEmail, bccEmail=bccEmail,
                          attachment_paths=attachment_paths)
            
    elif(choice == '2'):
        # email_view = input("Email view :")
        # if email_view =="":
        #     email_view = config.username
        getting.login(username=config.username)
        getting.getMail(username=config.username)

