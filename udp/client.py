import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("127.0.0.1", 9090)
sock.connect(addr)
print("Conectado")
sock.send("STOP".encode())
