import os
import config
import re

FILTERS = config.Boloc
def creatfolder(boxname):
    parent = os.getcwd()
    path = os.path.join(parent, boxname)
    if os.path.isdir(path):
        return False
    os.mkdir(path)
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
def Createboxes(ArrFil=FILTERS):
    for line in ArrFil:
        print(line)

print(taodanhsachloc())