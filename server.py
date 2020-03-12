
import socket
from threading import Thread
import threading
import logging 
import time
# Creates a socket



class ClienteThread(Thread):
    def __init__(self, ip, port, sock, filename, logger):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.filename=filename
        self.logger = logger
        self.logger.info("New thread started for "+ip+":"+str(port))

    def run(self):
        try:
            data = self.sock.recv(SIZE).decode()
            self.logger.info("Recibiendo Saludo Cliente")
            if data == HOLA:
                self.sock.send(CONECTADO.encode())
                self.logger.info("Enviando Confirmacion conexion")
            data = self.sock.recv(SIZE).decode()
            if data == LISTO:
                lk.acquire()
                clientes_listos += 1
                lk.release()
                self.logger.info("Cliente"+self.ip +" Listo para recibir archivos")
            else: 
                self.sock.close()
                self.logger.info("Se termino la conexión con "+ self.ip + "en el puerto "+ self.port )
                self.logger.info("Respuesta no esperada")
               
            while clientes_listos < n_clientes:
                self.logger.info("No se ha completado el numero de clientes")
                continue
            
            # enviar archivo
            if clientes_enviados < n_clientes:
                self.logger.info("Enviando archivo")
                lk2.acquire()
                clientes_enviados += 1
                lk2.release()

                f = open(self.filename,'rb')
                start_time = time.time()
                start_clock = time.clock()
                while True:
                    l = f.read(SIZE)
                    while l:
                        self.sock.send(l)
                        # print('Sent ',repr(l))

                        l = f.read(SIZE)
                    if not l:
                        f.close()
                        end_time = time.time()
                        end_clock = time.clock()
                        time_time = end_time-start_time
                        clock_time = end_clock-start_clock
                        self.sock.close()
                        self.logger.info("Envio Terminado con " + self.ip + "en el puerto "+ self.port)
                        self.logger.info("Se termino la conexión con "+ self.ip + "en el puerto "+ self.port )
                        self.logger.info("Clock duration "+ str(clock_time)  +" seconds process time")
                        self.logger.info("Time durattion "+ str(time_time) + " seconds wall time")
                        break
            else:
                self.logger.info("Se termino la conexión con "+ self.ip + "en el puerto "+ self.port )
                self.sock.close()
        except Exception as e:
            self.logger.error("Error: " + str(e))
            self.sock.close()

def create_socket(logger):
    try: 
        global host
        global port
        global s
        #ip fija del servidor
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
        s.bind((host,port))
        # se escucha para encontrar conexiones
        s.listen(25)
    except socket.error as msg:
        logger.error(("Socket binding error: " + str(msg)+"Retrying"))

        binding_socket(logger)

# acepta conexiones que esten en el puerto esperando
def accept_connections(logger):
    global n_clientes
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]
    filename = input("ingrese el nombre del archivo a enviar: ")
    while True:
        try:
            conn, address = s.accept()
            logger.info("La conexion se ha establecido: IP: "+address[0] + "en el puerto: " + str(address[1]))
            s.setblocking(1)
            all_connections.append(conn)
            all_address.append(address)
            tcliente= ClienteThread(address[0], port, conn,filename,logger)
            tcliente.start()
            clientesThreads.append(tcliente)
            lk2.acquire() 
            
            if clientes_enviados == n_clientes:
                lk2.release()
                lk3.acquire()
                n_clientes = int(input("Ingrese el numero de clientes a esperar para mandar el archivo:  "))
                lk3.release()
                for t in clientesThreads:
                    t.join()
                logger.info("Cerrando conexiones de clientes ")
                for c in all_connections:
                    c.close()
            else:
                lk2.release()
        except Exception as e:
            logger.error(str(e))
            for c in all_connections:
                c.close()

    # funcion

def create_server_log():
    fid= "log_server.txt"
    
    logging.basicConfig(filename=fid,level=logging.DEBUG)
    # create logger
    logger = logging.getLogger("server_logger")
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

    return logger

if __name__ == '__main__':
    global n_clientes
    global all_connections
    global all_address
    global SIZE
    n_clientes = int(input("Ingrese el numero de clientes a esperar para mandar el archivo:  "))


    all_connections = []
    all_address = []
    SIZE = 1024
    HOLA = "HOLA"
    CONECTADO = "CONECTADO"
    LISTO = "LISTO"
    clientes_listos = 0
    lk = threading.Lock()
    lk2 = threading.Lock()
    lk3=threading.Lock()
    clientesThreads=[]
    
    clientes_enviados = 0
    logger = create_server_log()
    create_socket(logger)
    binding_socket(logger)
    accept_connections(logger)