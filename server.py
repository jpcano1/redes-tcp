
import socket
from threading import Thread
import threading
import logging
import time
import hashlib
from datetime import datetime
# Creates a socket


class ClienteThread(Thread):
    def __init__(self, ip, port, sock, filename, logger):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.filename = filename
        self.logger = logger
        lk4.acquire()
        self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + datetime.today().strftime(
            '%Y-%m-%d-%H:%M:%S') + "New thread started for "+ip+":"+str(port))
        lk4.release()

    def run(self):
        global n_clientes

        global SIZE
        global clientes_listos
        global clientes_enviados
        try:
            data = self.sock.recv(SIZE).decode()
            lk4.acquire()
            self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Recibiendo Saludo de cliente: " + self.ip)
            lk4.release()
            if data == HOLA:
                self.sock.send(CONECTADO.encode())
                lk4.acquire()
                self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
                    "Enviando Confirmacion conexion a cliente: " + self.ip)
                lk4.release()
            data = self.sock.recv(SIZE).decode()
            if data == LISTO:
                lk.acquire()
                clientes_listos += 1
                lk.release()
                lk4.acquire()
                self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Cliente: "+self.ip +
                                 " Listo para recibir archivos")
                lk4.release()
            else:
                self.sock.close()
                lk4.acquire()
                self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Se termino la conexión con " +
                                 self.ip + "en el puerto " + int(self.port))
                self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Respuesta no esperada")
                lk4.release()

            while clientes_listos < n_clientes:
                lk4.acquire()
                self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "No se ha completado el numero de clientes")
                lk4.release()
                continue

            # enviar archivo
            lk3.acquire()
            lk2.acquire()
            lk.acquire()
            if clientes_enviados < n_clientes:
                lk4.acquire()
                self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Enviando archivo a cliente " + self.ip)
                lk4.release()
                clientes_listos -= 1
                clientes_enviados += 1
                lk3.release()
                lk2.release()
                lk.release()

                f = open(self.filename, 'rb')
                start_time = time.time()

                while True:
                    l = f.read(SIZE)
                    while l:
                        self.sock.send(l)
                        # print('Sent ',repr(l))

                        l = f.read(SIZE)
                    if not l:
                        f.close()

                        end_time = time.time()

                        time_time = end_time-start_time
                        lk4.acquire()
                        self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
                            "Envio Terminado con cliente: " + self.ip + "en el puerto " + str(self.port))
                        self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
                            "Se termino la conexión con cliente: " + self.ip + "en el puerto " + str(self.port))

                        self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
                            "Duracion: " + str(time_time) + " seconds wall time")
                        lk4.release()
                     

                        break
                h = hash_file(self.filename)
                print(h)
                self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
                            "Enviando Hash")
                self.sock.send("HASH".encode())
                self.sock.send(h.encode())
                resp = self.sock.recv(SIZE).decode()
                if resp=="ERROR":
                    lk4.acquire()
                    self.logger.info("El usuario con ip: "+ self.ip + "recibio el archivo mal")
                    lk4.release()
                else:
                    lk4.acquire()
                    self.logger.info("El usuario con ip: "+ self.ip + "recibio el archivo corrrecto")
                    lk4.release()
                self.sock.close()
            else:
                self.sock.close()
                lk2.release()
                lk3.release()
                lk.release()
                lk4.acquire()
                self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Se terminó la conexión con " +
                                 self.ip + "en el puerto " + str(self.port))
                lk4.release()

        except Exception as e:
            print(e)
            if not lk.acquire(False):
                lk.release()
            if not lk2.acquire(False):
                lk2.release()
            if not lk3.acquire(False):
                lk3.release()
            if not lk4.acquire(False):
                lk4.release()
            lk4.acquire()
            self.logger.error("Error: " + str(e))
            lk4.release()
            self.sock.close()


def create_socket(logger):
    try:
        global host
        global port
        global s
        # ip fija del servidor
        # host = "10.0.0.4"
        host = "localhost"
        port = 9090
        s = socket.socket()
        logger.info('Creando Socket')
    except socket.error as msg:
        logger.error("Socket creation error:  " + str(msg))

# binding socket listening for connections


def binding_socket(logger):
    try:
        global host
        global port
        global s

        logger.info("Binding port: "+str(port))
        # se une el puerto con el host
        s.bind((host, port))
        # se escucha para encontrar conexiones
        s.listen(25)
    except socket.error as msg:
        logger.error(("Socket binding error: " + str(msg)+"Retrying"))

        binding_socket(logger)

# acepta conexiones que esten en el puerto esperando


def accept_connections(logger):
    global n_clientes
    global all_connections
    global all_address
    global SIZE
    global clientes_listos
    global clientes_enviados
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]
    filename = input("Ingrese el nombre del archivo a enviar: ")
    while True:
        try:
            conn, address = s.accept()
            logger.info("La conexión se ha establecido: IP: " +
                        address[0] + " en el puerto: " + str(address[1]))
            s.setblocking(1)
            all_connections.append(conn)
            all_address.append(address)
            tcliente = ClienteThread(address[0], port, conn, filename, logger)
            tcliente.start()
            clientesThreads.append(tcliente)
            lk2.acquire()
            lk3.acquire()
            lk.acquire()
            lk4.acquire()
            if clientes_enviados == n_clientes:
               

                logger.info("Cerrando conexiones de clientes ")

                for c in all_connections:
                    c.close()
                clientes_enviados = 0

                clientes_listos = 0
                n_clientes=0
                while n_clientes == 0:
                    n_clientes = input(
                        "Ingrese el numero de clientes a esperar para mandar el archivo:  ")
                    n_clientes = int(n_clientes)
                lk2.release()
                lk.release()
                lk4.release()
                lk3.release()

            else:
                lk2.release()
                lk.release()
                lk4.release()
                lk3.release()

        except Exception as e:
            print(e)
            lk4.release()
            lk4.acquire()
            logger.error(str(e))
            lk4.release()
     
            if not lk.acquire(False):
                lk.release()
            if not lk2.acquire(False):
                lk2.release()
            if not lk3.acquire(False):
                lk3.release()
            if not lk4.acquire(False):
                lk4.release()

            for c in all_connections:
                c.close()

    # funcion


def create_server_log():
    fid = "log_server.txt"

    logging.basicConfig(filename=fid, level=logging.DEBUG)
    # create logger
    logger = logging.getLogger("server_logger")
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
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
    global n_clientes
    global all_connections
    global all_address
    global SIZE
    global clientes_listos
    global clientes_enviados
    n_clientes = int(
        input("Ingrese el numero de clientes a esperar para mandar el archivo:  "))

    all_connections = []
    all_address = []
    SIZE = 1024
    HOLA = "HOLA"
    CONECTADO = "CONECTADO"
    LISTO = "LISTO"
    clientes_listos = 0
    lk = threading.Lock()
    lk2 = threading.Lock()
    lk3 = threading.Lock()
    lk4 = threading.Lock()
    clientesThreads = []

    clientes_enviados = 0

    logger = create_server_log()
    create_socket(logger)
    binding_socket(logger)
    accept_connections(logger)
