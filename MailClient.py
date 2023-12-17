import config
import os
class MailClient:
    def __init__(self, sender="", to_addresses=[], cc_addresses=[], bcc_addresses=[], subject="", body="",uid =""):
        self.sender = sender
        self.to_addresses = to_addresses
        self.cc_addresses = cc_addresses
        self.bcc_addresses = bcc_addresses
        self.subject = subject
        self.body = body
        self.isRead = False
        self.uid = uid
    def display_brief(self,num):
        isread = "(not read)" if self.isRead == False else ""
        print(f"{num}. {isread} <{self.sender}>, <{self.subject}>")

    def display_info(self):
        # print(f"From: {self.sender}")
        # print(f"To: {', '.join(self.to_addresses)}")
        # if self.cc_addresses:
        #     print(f"CC: {', '.join(self.cc_addresses)}")
        # if self.bcc_addresses:
        #     print(f"BCC: {', '.join(self.bcc_addresses)}")
        print(f"Subject: {self.subject}")
        print(f"Body: {self.body}")
    def getStrInfo(self):
        result = ""
        # result += f"From: {self.sender}\n"
        # result += f"To: {', '.join(self.to_addresses)}\n"
        # if self.cc_addresses:
        #     result += f"CC: {', '.join(self.cc_addresses)}\n"
        # if self.bcc_addresses:
        #     result += f"BCC: {', '.join(self.bcc_addresses)}\n"
        result += f"Subject: {self.subject}\n"
        result += f"Body: {self.body}\n"
        return result
    def getFolderType(self):
        type = "Inbox"
        if "ahihi@testing.com"==self.sender or "ahuu@testing.com"==self.sender :
            type = "Project"
        elif "urgent" in self.subject or "ASAP" in self.subject :
            type = "Important"
        elif "report" in self.body or "meeting" in self.body :
            type = "Work"
        elif ("virus" in self.body or "virus" in self.subject 
            or "hack" in self.body or "hack" in self.subject
            or "crack" in self.body or "crack" in self.subject) :
            type = "Spam"
        return type
    def checkRead(self):
        path = f"{config.folderpath}/{config.username}/{self.getFolderType()}/{self.uid}.txt"
        if os.path.exists(path) :
            return True
        return False     