
import socket
from threading import Thread
import threading
import logging
import time
import hashlib
from datetime import datetime
from time import sleep
# Creates a socket

class ClienteThread(Thread):
    def __init__(self,message, ip, sock,filename, logger):
        Thread.__init__(self)
        self.ip = ip
        self.message=message
        self.sock = sock
        self.filename = filename
        self.port=ip[1]
        self.logger = logger
        lk4.acquire()
        self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + datetime.today().strftime(
            '%Y-%m-%d-%H:%M:%S') + "New thread started for "+ip[0]+":")
        lk4.release()

    def run(self):
        handle_cliente_request(self.message.decode(),self.sock,self.ip,self.logger,self.filename)
        sleep(0.5)
        # global n_clientes

        # global SIZE
        # global clientes_listos
        # global clientes_enviados
        # try:
        #     data = self.message.decode()
            
        #     if data == HOLA:
        #         lk4.acquire()
        #         self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Recibiendo Saludo de cliente: " + self.ip[0])
        #         lk4.release()
        #         self.sock.sendto(CONECTADO.encode(),self.ip)
        #         lk4.acquire()
        #         self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
        #             "Enviando Confirmacion conexion a cliente: " + self.ip[0])
        #         lk4.release()
            
            
        #     data = self.sock.recv(SIZE).decode()
        #     if data == LISTO:
        #         lk.acquire()
        #         clientes_listos += 1
        #         lk.release()
        #         lk4.acquire()
        #         self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Cliente: "+self.ip[0] +
        #                          " Listo para recibir archivos")
        #         lk4.release()
        #     else:
        #         self.sock.close()
        #         lk4.acquire()
        #         self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Se termino la conexión con: " +
        #                          self.ip + "en el puerto: " + int(self.port))
        #         self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + " Respuesta no esperada")
        #         lk4.release()

        #     while clientes_listos < n_clientes:
        #         lk4.acquire()
        #         #self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + " No se ha completado el numero de clientes")
        #         lk4.release()
        #         continue

        #     # enviar archivo
        #     lk3.acquire()
        #     lk2.acquire()
        #     lk.acquire()
        #     if clientes_enviados < n_clientes:
        #         lk4.acquire()
        #         self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + " Enviando archivo a cliente: " + self.ip[0])
        #         lk4.release()
        #         clientes_listos -= 1
        #         clientes_enviados += 1
        #         lk3.release()
        #         lk2.release()
        #         lk.release()
        #         self.sock.sendto((self.filename[:-4]+str(clientes_enviados)+self.filename[self.filename.find('.')::]).encode(),self.ip)
        #         f = open(self.filename, 'rb')
        #         start_time = time.time()

                
        #         l = f.read(SIZE)
        #         while l:
        #             self.sock.sendto(l,self.ip)
        #             # print('Sent ',repr(l))

        #             l = f.read(SIZE)
        #         if not l:
        #             f.close()

        #             end_time = time.time()

        #             time_time = end_time-start_time
        #             lk4.acquire()
        #             self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
        #                 " Envio Terminado con cliente: " + self.ip[0] + "en el puerto: " + str(self.port))
                    
        #             self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
        #                 "Duracion: " + str(time_time) + " seconds wall time")
        #             lk4.release()

        #             h = hash_file(self.filename)
        #             print(h)
        #             self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +
        #                         " Enviando Hash")
        #             sleep(1)
        #             self.sock.sendto("HASH".encode(),self.ip)
        #             data = self.sock.recv(SIZE).decode()
        #             if data == LISTO:
        #                 self.sock.sendto(h.encode(),self.ip)
        #             resp = self.sock.recv(SIZE).decode()
        #             if resp=="ERROR":
        #                 lk4.acquire()
        #                 self.logger.info("El usuario con ip: "+ self.ip[0] + " recibio el archivo mal")
        #                 lk4.release()
        #             else:
        #                 lk4.acquire()
        #                 self.logger.info("El usuario con ip: "+ self.ip[0] + " recibio el archivo correcto")
        #                 lk4.release()
        #             self.sock.close()
        #     else:
        #         self.sock.close()
        #         lk2.release()
        #         lk3.release()
        #         lk.release()
        #         lk4.acquire()
        #         self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + " Se terminó la conexión con: " +
        #                          self.ip[0] + " en el puerto: " + str(self.port))
        #         lk4.release()

        # except Exception as e:
        #     print(e)
        #     if not lk.acquire(False):
        #         lk.release()
        #     if not lk2.acquire(False):
        #         lk2.release()
        #     if not lk3.acquire(False):
        #         lk3.release()
        #     if not lk4.acquire(False):
        #         lk4.release()
        #     lk4.acquire()
        #     self.logger.error("Error: " + str(e))
        #     lk4.release()
        #     self.sock.close()


def create_socket(logger):
    try:
        global host
        global port
        global s
        # ip fija del servidor
        # host = "172.19.255.255"
        host = "0.0.0.0"
        port = 9090
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        logger.info('Creando Socket')
    except socket.error as msg:
        logger.error("Socket creation error: " + str(msg))

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
        # s.listen(25)
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
    filename = input("Ingrese el nombre del archivo a enviar, presione intro si quiere dejar uno predeterminado: ")
    if filename == '':
        filename = 'prueba.txt'
    while True:
        try:
            #conn, address = s.accept()
            # logger.info("La conexión se ha establecido: IP: " +
            #             address[0] + " en el puerto: " + str(address[1]))
            s.setblocking(1)
            recvdata,addr = s.recvfrom(SIZE)
            # all_connections.append(conn)
            # all_address.append(address)
            tcliente = ClienteThread(recvdata,addr,s, filename, logger)
            tcliente.start()
            clientesThreads.append(tcliente)
            sleep(1)
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


def handle_cliente_request(data,sock,ip,logger,filename):
    global n_clientes

    global SIZE
    global clientes_listos
    global clientes_enviados
    try:
        if data == HOLA:
            lk4.acquire()
            logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Recibiendo Saludo de cliente: " + ip[0])
            lk4.release()
            lk_sock.acquire()
            sock.sendto(CONECTADO.encode(),ip)
            lk_sock.release()
            lk4.acquire()
            logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
                "Enviando Confirmacion conexion a cliente: " + ip[0])
            lk4.release()
        elif data==LISTO:
            lk.acquire()
            clientes_listos += 1
            lk.release()
            lk4.acquire()
            logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "Cliente: "+ip[0] +
                                " Listo para recibir archivos")
            lk4.release()

            while clientes_listos < n_clientes:
                lk4.acquire()
                #self.logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + " No se ha completado el numero de clientes")
                lk4.release()
                continue

            lk3.acquire()
            lk2.acquire()
            lk.acquire()
            if clientes_enviados < n_clientes:
                lk4.acquire()
                logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + " Enviando archivo a cliente: " + ip[0])
                lk4.release()
                clientes_listos -= 1
                clientes_enviados += 1
                lk3.release()
                lk2.release()
                lk.release()
                lk_sock.acquire()
                sock.sendto((filename[:-4]+'_'+str(clientes_enviados)+filename[filename.find('.')::]).encode(),ip)
                lk_sock.release()
                f = open('./data/'+filename, 'rb')
                start_time = time.time()

                
                l = f.read(SIZE)
                while l:
                    lk_sock.acquire()
                    sock.sendto(l,ip)
                    lk_sock.release()
                    # print('Sent ',repr(l))

                    l = f.read(SIZE)
                if not l:
                    f.close()

                    end_time = time.time()

                    time_time = end_time-start_time
                    lk4.acquire()
                    logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
                        " Envio Terminado con cliente: " + ip[0] + "en el puerto: " + str(ip[1]))
                    
                    logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + 
                        "Duracion: " + str(time_time) + " seconds wall time")
                    lk4.release()

                    h = hash_file('./data/'+filename)
                    print(h)
                    logger.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +
                                " Enviando Hash")
                    sleep(1)
                    lk_sock.acquire()
                    sock.sendto("HASH".encode(),ip)
                    lk_sock.release()
                    lk_sock.acquire()
                    data = sock.recv(SIZE).decode()
                    lk_sock.release()
                    if data == LISTO:
                        lk_sock.acquire()
                        sock.sendto(h.encode(),ip)
                        lk_sock.release()
                    lk_sock.acquire()
                    resp = sock.recv(SIZE).decode()
                    lk_sock.release()
                    if resp=="ERROR":
                        lk4.acquire()
                        logger.info("El usuario con ip: "+ ip[0] + " recibio el archivo mal")
                        lk4.release()
                    else:
                        lk4.acquire()
                        logger.info("El usuario con ip: "+ ip[0] + " recibio el archivo correcto")
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
            if not lk_sock.acquire(False):
                lk_sock.release()
            lk4.acquire()
            logger.error("Error: " + str(e))
            lk4.release()
           

                    
   


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
    lk_sock=threading.Lock()
    clientesThreads = []

    clientes_enviados = 0

    logger = create_server_log()
    create_socket(logger)
    binding_socket(logger)
    accept_connections(logger)



