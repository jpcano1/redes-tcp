import socket
import logging

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
        with open('received_file.txt', 'wb') as f:
            print( 'file opened')
            while True:
                #print('receiving data...')
                data = s.recv(1024)
                # print('data=%s'%(data))
                if not data:
                    f.close()
                    print ('file close()')
                    break
                # write data to a file
                f.write(data)

def create_client_log():
    fid = "log_client.txt"
    logging.basicConfig(filename=fid, )

if __name__ == '__main__':
    s = socket.socket()
    host = input("Ingrese el host de conexión ej: 'localhost': ")
    # host = "localhost"
    port = 9090
    s.connect((host, port))
    print("Conectado")
    cliente = Cliente(s)
    cliente.procesar()