import sendmail as sending
import config

choice = '0'
while(choice != '3'):
    print("1.Send email")
    print("2.Get email")
    print("3.Exit")
    choice = input("Enter your choice : ")
    print(choice)
    if(choice =='3'): 
        break
    elif(choice == '1'):
        email_receiver = input("Email receiver : ")
        email_receiver = [email.strip() for email in email_receiver.split(',')]
        email_subject = input("Email subject : ")
        email_msg = input("Email message : ")
        sending.send_mail(subject=email_subject,from_addr=config.username,to_addr=email_receiver,msg=email_msg)
sending.quit()