import socket
import logging
import time
from datetime import datetime

from threading import Thread
HOLA = "HOLA"
SIZE = 1024
CONECTADO = "CONECTADO"
LISTO = "LISTO"

class Cliente:

    def __init__(self, sock: socket.socket, logger):
        self.sock = sock
        self.logger = logger

    def procesar(self):
        self.sock.send(HOLA.encode())
        data = self.sock.recv(SIZE).decode()
        if data == CONECTADO:
            self.sock.send(LISTO.encode())
            self.logger.info("Conectado con el servidor")
        data = self.sock.recv(SIZE).decode()
        start_time = time.time()
        with open('received_file.txt', 'wb') as f:
            print( 'file opened')
            self.logger.info("Se empezó a recibir el archivo")
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
            end_time = time.time()
            time_time = end_time - start_time
            self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +
                             "Duracion: " + str(time_time) + " seconds wall time")

def create_client_log():
    fid = "log_client.txt"
    logging.basicConfig(filename=fid, level=logging.DEBUG)

    logger = logging.getLogger('client_logger')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

if __name__ == '__main__':
    s = socket.socket()
    host = input("Ingrese el host de conexión ej: 'localhost': ")
    # host = "localhost"
    port = 9090
    logger = create_client_log()
    s.connect((host, port))
    print("Conectado")
    logger.info("Cliente conectado")
    cliente = Cliente(s, logger)
    cliente.procesar()