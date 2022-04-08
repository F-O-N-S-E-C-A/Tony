import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1999  # The port used by the server

boxes = {"fruit": "ba721314-b4b8-11ec-ad41-acde48001122",
         "vodka": "ba683fec-b4b8-11ec-ad41-acde48001122",
         "whiskey": "ba6ddf56-b4b8-11ec-ad41-acde48001122",
         "pizza": "ba6f4346-b4b8-11ec-ad41-acde48001122",
         "arduino components": "ba70a89e-b4b8-11ec-ad41-acde48001122",
         "donut": "ba74fc46-b4b8-11ec-ad41-acde48001122"}


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    DATA = "FIND:" + boxes["donut"]
    s.sendall(DATA.encode())
    #data = s.recv(1024)

    #print(data.decode())