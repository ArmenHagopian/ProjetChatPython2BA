# adder.py
# authors: Armen Hagopian, Gaétan Guru
# version: February 26, 2016

import threading
import pickle
import socket
import struct
import sys

SERVERADDRESS = (socket.gethostname(), 6000)
clientslist = dict()
clientslist["connectedclients"] = dict()


class AdderServer():

    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        print('Clients connectés : ')

#The fonction run() listens to a client. When there's a client connected, run() triggers the function handle.

    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                self._handle(client)
                client.close()
            except OSError:
                print('Erreur lors du traitement de la requête du client.')

#The function handle() saves the ip address, the port, the name of the person if precised into a dictionnary. 
#Then, It immediately sends back the dictionnary to the active client who's ready to chat.


    def _handle(self, client):
        clientnumber = 1
        size = struct.unpack('I', client.recv(4))[0]
        data = pickle.loads(client.recv(size))
        result = ''
        ip = data[0]
        port = data[1]
        if len(data[0]) < len(data[1]):
            ip = data[1]
            port = data[0]
        print('\t' + ip, port)
        if clientslist["connectedclients"]:
            clients = clientslist["connectedclients"]
            for i in clientslist["connectedclients"]:
                if len(clients[i]) == 3:
                    result += '\n' + '\t' + 'Client n°{}, {} : Adresse IP : {} \n\t\t     Numéro de port : {}'.format(
                    clientnumber, clients[i][2], str(clients[i][0]), str(clients[i][1]))
                    clientnumber += 1
                else:
                    result += '\n' + '\t' + 'Client n°{} : Adresse IP : {} \n\t\t     Numéro de port : {}'.format(
                    clientnumber, str(clients[i][0]), str(clients[i][1]))
                    clientnumber += 1

        else:
            result = '\n' + '\t' + 'Aucun client connecté pour le moment'
        clientslist["connectedclients"]['Client n°{}'.format(clientnumber)] = [ip, port]
        if len(data) == 3:
            clientslist["connectedclients"]['Client n°{}'.format(clientnumber)] = [ip, port, data[2]]

        print(clientslist)
        client.send(str(result).encode())


class AdderClient():

    def __init__(self, address):
        self.__data = [x for x in address]
        self.__s = socket.socket()
        
#The function run(self) triggers the function compute(self) if everything goes as expected. In the other case, It rejects an exception. 

    def run(self):
        try:
            self.__s.connect(SERVERADDRESS)
            print('Clients connectés : ', self._compute())
            self.__s.close()
        except OSError:
            print('Serveur introuvable, connexion impossible.')
            
 #The function compute(self) sends the ip address, the port, the name (if precised) of the client to the server. 
#It also returns the data that is sent from the server.

    def _compute(self):
        try:
            totalsent = 0
            msg = pickle.dumps(self.__data)
            self.__s.send(struct.pack('I', len(msg)))
            while totalsent < len(msg):
                sent = self.__s.send(msg[totalsent:])
                totalsent += sent
            return self.__s.recv(1024).decode()
        except OSError:
            print("Erreur lors de la récupération du message.")


class Chat():

    def __init__(self, host=socket.gethostname(), port=7000):
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, port))
        self.__s = s
        print('Écoute sur {}:{}'.format(host, port))

#The function run(self) triggers an infinite loop in which It is possible to activate 4 commands. 

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send
        }
        self.__running = True
        self.__address = None
        threading.Thread(target=self._receive).start()
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ')+1:].rstrip()
            # Call the command handler
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                    print("Erreur lors de l'exécution de la commande.")
            else:
                print('Commande inconnue:', command)
#The function _exit(self) exits the running program.

    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()

#The function _quit(self) closes the connection between the 2 peers.

    def _quit(self):
        self.__address = None

#The function _join(self) enables us to join another peer 

    def _join(self, param):
        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                self.__address = (tokens[0], int(tokens[1]))
                print('Connecté à {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur lors de l'envoi du message.")

#The function _send(self,param) enables us to send data towards a peer 


    def _send(self, param):
        if self.__address is not None:
            try:
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
            except OSError:
                print('Erreur lors de la réception du message.')

#The function _receive(self) enables us to receive data from a peer

    def _receive(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(1024)
                print(data.decode())
            except socket.timeout:
                pass
            except OSError:
                return

if __name__ == '__main__':

    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        AdderServer().run()

    elif len(sys.argv) == 5 and sys.argv[1] == 'client':
        if sys.argv[2] == 'ECAM':
# We change the parameters of the classes depending on which parameter (ip address or port) the user gives first
            if len(sys.argv[3]) > len(sys.argv[4]):
                AdderClient(sys.argv[3:]).run()
                Chat(sys.argv[3], int(sys.argv[4])).run()
            elif len(sys.argv[3]) < len(sys.argv[4]):
                AdderClient(sys.argv[3:]).run()
                Chat(sys.argv[4], int(sys.argv[3])).run()
    elif len(sys.argv) == 6 and sys.argv[1] == 'client':
        if sys.argv[2] == 'ECAM':
# We change the parameters of the classes depending on which parameter (ip address or port) the user gives first
            if len(sys.argv[3]) > len(sys.argv[4]):
                AdderClient(sys.argv[3:]).run()
                Chat(sys.argv[3], int(sys.argv[4])).run()
            elif len(sys.argv[3]) < len(sys.argv[4]):
                AdderClient(sys.argv[3:]).run()
                Chat(sys.argv[4], int(sys.argv[3])).run()
    elif len(sys.argv) == 8 and sys.argv[1] == 'client':
        if sys.argv[2] == 'ECAM':
# In case the server is on another computer (with a different address), the client specifies the server's ip
# address and port
            if len(sys.argv[3]) > len(sys.argv[4]):
                SERVERADDRESS = (sys.argv[5], sys.argv[6])
                AdderClient(sys.argv[3:5]).run()
                Chat(sys.argv[3], int(sys.argv[4])).run()
            elif len(sys.argv[3]) < len(sys.argv[4]):
                SERVERADDRESS = (sys.argv[5], sys.argv[6])
                AdderClient(sys.argv[3:5]).run()
                Chat(sys.argv[4], int(sys.argv[3])).run()
        else:
            print("Veuillez entrer un mot de passe valide ou entrer la commande sous la forme :\n"
                  "'python3 adder.py client «MotDePasse» «Votre Adresse IP» «Numéro de Port»' ")

    elif len(sys.argv) == 4 and sys.argv[1] == 'peer':
        Chat(sys.argv[2], int(sys.argv[3])).run()

