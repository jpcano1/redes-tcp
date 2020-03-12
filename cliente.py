import socket
from threading import Thread

HOLA = "HOLA"
SIZE = 1024
CONECTADO = "CONECTADO"
LISTO = "LISTO"

class Cliente:

    def __init__(self, sock: socket.socket):
        self.sock = sock

    def procesar(self):
        self.sock.send(HOLA.encode())
        data = self.sock.recv(SIZE).decode()
        if data == CONECTADO:
            self.sock.send(LISTO.encode())
        data = self.sock.recv(SIZE).decode()
        print(data)

if __name__ == '__main__':
    s = socket.socket()
    # host = input("Ingrese el host de conexion ej: 'localhost': ")
    host = "localhost"
    port = 9090
    s.connect((host, port))
    print("Conectado")
    cliente = Cliente(s)
    cliente.procesar()
    s.close()


