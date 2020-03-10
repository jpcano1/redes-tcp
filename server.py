
import socket
import sys
from threading import Thread
import threading
# Creates a socket

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []
SIZE = 1024
HOLA = "HOLA"
CONECTADO = "CONECTADO"
LISTO = "LISTO"
clientes_listos = 0
lk = threading.Lock()
lk2 = threading.Lock()
n_clientes = int(input("Ingrese el numero de clientes a esprear para mandar el archivo"))
clientes_enviados = 0
class ClienteThread(Thread):
    def __init__(self, ip, port, sock, cl):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print ("New thread started for "+ip+":"+str(port))

    def run(self):
        try:
            data = self.sock.recv(SIZE).decode()
            if data == HOLA:
                self.sock.send(CONECTADO.encode())
            data = self.sock.recv(SIZE).decode()
            if data == LISTO:
                lk.acquire()
                clientes_listos += 1
                lk.release()
            else: 
                self.sock.close()
               
            while clientes_listos < n_clientes:
                continue
            
            # enviar archivo
            if clientes_enviados < n_clientes:
                lk2.acquire()
                clientes_enviados += 1
                lk2.release()

            

                filename = 'mytext.txt'
                f = open(filename,'rb')
                while True:
                    l = f.read(SIZE)
                    while l:
                        self.sock.send(l)
                        # print('Sent ',repr(l))
                        l = f.read(SIZE)
                    if not l:
                        f.close()
                        self.sock.close()
                        break
            else:
                self.sock.close()
        except:
          print("Error")

def create_socket():
    try: 
        global host
        global port
        global s
        #ip fija del servidor
        host = "localhost"
        port = 9090
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error:  " + str(msg))

# binding socket listening for connections
def binding_socket():
    try: 
        global host
        global port
        global s

        print("Binding port"+str(port))
        # se une el puerto con el host
        s.bind((host,port))
        # se escucha para encontrar conexiones
        s.listen(25)
    except socket.error as msg:
        print("Socket binding error:  " + str(msg)+"Retrying")

        binding_socket()

# acepta conexiones que esten en el puerto esperando
def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            print("La conexion se ha establecido: IP:"+address[0] + "en el puerto" + str(address[1]))
            s.setblocking(1)  
            all_connections.append(conn)
            all_address.append(address)
            tcliente= ClienteThread(address, port, conn)
            t.start()
            
        except Exception as e:
            pass
    # funcion
