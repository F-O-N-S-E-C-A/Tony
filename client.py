import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

boxes = ["ba721314-b4b8-11ec-ad41-acde48001122", "ba6ddf56-b4b8-11ec-ad41-acde48001122"]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    DATA = "FIND:" + boxes[1]
    s.sendall(DATA.encode())
    #data = s.recv(1024)

    #print(data.decode())