import json
config_path = "config.json"
with open(config_path,'r') as file:
    config = json.load(file)
username = config["Username"]
password = config["Password"]
mailServer = config["MailServer"]
smtp = config["SMTP"]
pop3 = config["POP3"]
autoload = config["Autoload"]