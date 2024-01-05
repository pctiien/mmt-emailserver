import email.parser
import os
import config
import re
from email import policy
FILTERS = config.Boloc
def creatfolder(boxname):
    parent = os.getcwd()
    parent=os.path.join(parent,"Home")
    path = os.path.join(parent, boxname)
    if os.path.isdir(path):
        return False
    os.makedirs(path)
    return True

def taodanhsachloc(ArrFilters=FILTERS):
    ret=[]
    pattern = "From|Subject|Content|Spam"
    for fi in ArrFilters:
        phanloai={}
        tach=fi.split('-')
        folder=tach[1]
        signs=tach[0]
        m=re.search(pattern,signs,re.IGNORECASE) #Do cac field quy uoc la khong phan biet hoa thuong(RFCs)
        fieldname=m.group()
        phanloai['field']=fieldname
        phanloai['keywords']=[]
        arrKey=signs[m.end():].split(',')
        for key in arrKey:
            phanloai['keywords'].append(key.strip(" \":"))
        m=re.search("To folder: ",folder)
        phanloai["mailbox"]=folder[m.end():]
        ret.append(phanloai)
    return ret
def Createboxes(danhsach):
    for line in danhsach:
        creatfolder(line['mailbox'])
    creatfolder('Inbox')

def TakeFolderName():
    parent = os.getcwd()
    path = os.path.join(parent, "Home")
    temp = os.listdir(path)
    return temp

def take_attachment(content, filename):
  # Lưu tệp đính kèm
  path = os.getcwd()
  dict["filename"]=filename
  path = os.path.join(path, "attach/" + filename)
  direct = os.path.dirname(path)
  if not os.path.exists(direct):
    os.makedirs(direct)
  with open(path, 'wb') as f:
    f.write(content)
def process_part(part):
    # Xử lý nội dung của từng phần trong multipart
    content=''
    attachment=()
    content_type = part.get_content_type()
    content_disposition = part.get("Content-Disposition", "")  # Tham số 2 là failobj
    # Thực hiện xử lý tùy thuộc vào content_type và content_disposition
    if "attachment" in content_disposition:
        # Xử lý tệp đính kèm
        attachment+=(part.get_filename(),)
        attachment+=(part.get_payload(decode=True),) # Decode dựa trên Content-Transfer-Encoding
    else:
        # Xử lý phần khác của multipart
        content=part.get_payload()
    return content,attachment


def Find(message_object,content,field,keywords):
    ret=False
    if field.casefold()!="Content".casefold():
        for i in keywords:
            ret=(message_object[field].find(i)>=0)#Trả về true nếu tìm thấy keyword
            if ret==True:
                break
    else:
        for i in keywords:
            ret = (content.find(i) >= 0)  # Trả về true nếu tìm thấy keyword
            if ret == True:
                break
    return ret

danhsach = taodanhsachloc()#Bắt buộc phải gọi đầu tiên, mỗi khi chạy đều tạo mới danh sách
Createboxes(danhsach)#Bắt buộc phải gọi thứ hai,tạo thư mục nếu chưa có
def locthu(message):
    flag=False
    message_object = email.message_from_string(message, policy=email.policy.default)
    subject = message_object['subject']
    if subject is None:
        subject="NO SUBJECT"
    sender = message_object["from"]
    text="FROM: "+message_object["from"]+"\nTO: "+message_object["To"]+"\n"
    if message_object["cc"]!= None:
        text+="CC: "+message_object["bbc"]+"\n"
    if message_object["bbc"]!= None:
        text+="BBC: "+message_object["bbc"]+'\n'
    text+="SUBJECT: "+subject+"\r\n\r\n"
    content=''
    attachment=[]
    if message_object.is_multipart():
        # Nếu là multipart, duyệt qua các phần và xử lý
        for part in message_object.walk():
            sub_content,sub_attachment = process_part(part)
            if sub_attachment:
                attachment.append(sub_attachment)
            if sub_content:
                content = sub_content
    else:
        # Nếu không phải là multipart, xử lý nội dung đơn
        sub_content,sub_attachment=process_part(message_object)
        if sub_attachment:
            attachment.append(sub_attachment)
        if sub_content:
            content = sub_content
    content=content.replace('\n.\n','')
    content=content.replace('\r\n.\r\n','')
    text+="CONTENT: "+content+"\n"
    for i in danhsach:
        keywords=i["keywords"]
        if i['field'].casefold()=="Spam".casefold():
            flag=Find(message_object,content,"Subject",keywords)
            if flag==True:
                break
            flag=Find(message_object,content,"Content",keywords)
        else:
            flag=Find(message_object,content,i["field"], keywords)
        if flag==True:
            break
    if flag == True:
        return i["mailbox"],sender,subject,text,attachment
    else:
        return "Inbox",sender,subject,text,attachment



