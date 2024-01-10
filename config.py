import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_directory, 'config.json')

with open(config_path, 'r') as file:
    config = json.load(file)
username = config["Username"]
password = config["Password"]
mailServer = config["MailServer"]
smtp = config["SMTP"]
pop3 = config["POP3"]
autoload = config["Autoload"]
Boloc = config["Filter"]