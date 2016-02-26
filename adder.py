
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
        self.__a = 2

    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                self.__a += 20
                self._handle(client)
                client.close()
            except OSError:
                print('Erreur lors du traitement de la requête du client.')

    def _handle(self, client):
        size = struct.unpack('I', client.recv(4))[0]
        data = pickle.loads(client.recv(size))
        result = ''
#Changer la ligne qui suit !!!
        clientslist["connectedclients"]['{} {}'.format(socket.gethostname(), self.__a)] = 2
        for i in clientslist["connectedclients"]:
            result += '{} {}'.format('\n' + '\t' + str(i), str(clientslist["connectedclients"][i]))
        print('Clients connectés : {} = {}'.format(data, result))
        client.send(str(result).encode())


class AdderClient():

    def __init__(self, message):
        self.__data = [int(x) for x in message]
        self.__s = socket.socket()

    def run(self):
        try:
            self.__s.connect(SERVERADDRESS)
            print('Clients connectés : ', self._compute())
            self.__s.close()
        except OSError:
            print('Serveur introuvable, connexion impossible.')

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

    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()

    def _quit(self):
        self.__address = None

    def _join(self, param):
        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                self.__address = (tokens[0], int(tokens[1]))
                print('Connecté à {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur lors de l'envoi du message.")

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
    elif len(sys.argv) > 2 and sys.argv[1] == 'client':
        AdderClient(sys.argv[2:]).run()
    elif len(sys.argv) == 4 and sys.argv[1] == 'peer':
        Chat(sys.argv[2], int(sys.argv[3])).run()