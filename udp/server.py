import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("127.0.0.1", 9090)
sock.bind(address)

while 1:
    data = sock.recv(1024).decode()
    if data == "STOP":
        print("Detenido")
        break
    print(data)