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

def Filter(ArrFilters=FILTERS):
    pattern = "From|Subject|Content|Spam"

    for fi in ArrFilters:
        re.split(pattern,fi,re.IGNORECASE) #Do cac field quy uoc la khong phan biet hoa thuong(RFCs)

def Createboxes(ArrFil=FILTERS):
    for line in ArrFil:
        print(line)

Filter()
