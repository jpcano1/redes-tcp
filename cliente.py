import socket
import logging
import time
from datetime import datetime
import hashlib

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
        FILENAME= self.sock.recv(SIZE).decode()
        self.logger.info("El nombre del archivo es: " + FILENAME)
        start_time = time.time()
        data =self.sock.recv(SIZE)
        try:
           
            with open(FILENAME, 'wb') as f:
                print( 'file opened')
                self.logger.info("Se empezó a recibir el archivo")
                while True:
                    print('receiving data...')
                    
                    if data.decode()=="HASH":
                        print("Se va a recibir el hash")
                        f.close()
                        self.logger.info("Se termino de recibir el archivo")
                        end_time = time.time()
                        time_time = end_time - start_time
                        self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +
                                        " Duracion: " + str(time_time) + " seconds wall time")
                        print ('file close()')
                        h=self.sock.recv(1024).decode()
                        print(h)
                        h_received = hash_file(FILENAME)
                        print(h_received)
                        self.logger.info("Recibiendo hash del archivo y verificando")
                        mes = "ERROR"

                        if h == h_received:
                            self.logger.info("El archivo llego correctamente")
                            mes= "CORRECTO"
                        else:
                            self.logger.info("El archivo llego mal")
                        self.sock.send(mes.encode())
                        break
                    # write data to a file
                    f.write(data)
                    data = self.sock.recv(SIZE)
        except Exception as e:
            print(e)
       

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

def hash_file(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:

        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()

if __name__ == '__main__':
    s = socket.socket()
    host = input("Ingrese el host de conexión, presione intro si quiere dejar uno predeterminado: ")
    if host == '':
        host = '127.0.0.1'
    # host = "localhost"
    port = 9090
    logger = create_client_log()
    s.connect((host, port))
    print("Conectado")
    logger.info("Cliente conectado")
    cliente = Cliente(s, logger)
    cliente.procesar()