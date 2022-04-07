import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

print("Server")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode("utf-8").split(":")
                if data[0] == "FIND":
                    id = data[1]
                    print("Find box with id: ", id)
            #conn.sendall(data.encode()