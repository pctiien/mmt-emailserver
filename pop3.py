from socket import *

import config

bufferSize = 1024
import email


def recv_msg():
  try:
    return client_socket.recv(bufferSize).decode()
  except timeout:
    return None

def send_msg(message, expect_return_msg=False):
  client_socket.sendall(f"{message}\r\n".encode())
  recv = recv_msg()
  if expect_return_msg:
    print(recv)
  return recv

host = config.mailServer
port = config.pop3
username = config.username
password = config.password
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((host,port))
print(client_socket.recv(1024).decode())
send_msg(f"USER {username}",True)
print(password)
send_msg(f"PASS {password}",True)
list = send_msg(f"LIST")
print (list)
client_socket.sendall(b"RETR 1\r\n")
#send_msg("QUIT")
fragments = []
while True:
  chunk = client_socket.recv(1024).decode()
  if not chunk:  # Cài đặt cho lần nhận đầu tiên không có data nào sẽ thoát
    break
  fragments.append(chunk)
  if chunk[-5:] == "\r\n.\r\n":  # Khi nhan mot goi tin lon, den luc da nhan đủ không còn data,
    break  # EOF. No more data           ham recv khong trả về '' mà đợi, vì thế có hai if
message = "".join(fragments)

file=open("message.txt","wt",newline='')
message=message.split('\n',1)[1]
file.write(message)
file.close()


def process_multipart_email(filename):
  # Sử dụng BytesParser để phân tích cú pháp email từ dữ liệu nhị phân
  msg = email.message_from_file(open(filename,'rt'))

  # Hiển thị các tiêu đề của email
  print("Subject:", msg["Subject"])
  print("From:", msg["From"])
  print("To:", msg["To"])

  # Xử lý các phần của email
  for part in msg.iter_parts():
    if part.is_multipart():
      # Đây là một phần multipart, bạn có thể xử lý nó tùy ý
      print("Found multipart part")
    else:
      # Đây là một phần đơn lẻ, có thể là văn bản, hình ảnh, hoặc đính kèm khác
      content_type = part.get_content_type()
      content_disposition = part.get("Content-Disposition", "")

      print(f"Content-Type: {content_type}")
      print(f"Content-Disposition: {content_disposition}")

      # Hiển thị nội dung nếu đó là văn bản
      if content_type == "text/plain" or content_type == "text/html":
        part.get_payload()
        print(part.get_payload())
      else:
        # Đây có thể là xử lý cho các loại nội dung khác tùy thuộc vào nhu cầu của bạn
        pass



# print(send_msg("UIDL"))
# print(repr(send_msg("TOP 3 0")))
# print(config.Boloc)





