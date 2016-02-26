import socket
import sys
import threading
import struct
import pickle

# faire en sort d'avoir le mm serveur pour EchoServer et EchoClient
clientslist = dict()
clientslist["connectedclients"] = dict()
SERVERADDRESS = ('192.168.1.9', 6000)


class EchoServer():
    def __init__(self, host=socket.gethostname(), port=6000):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)

    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            self._handle(client)
            client.close()

    def _handle(self, client):
        size = struct.unpack('I', client.recv(1))[0]
        data = pickle.loads(client.recv(size))
        result = sum(data)
        print('Somme de {} = {}'.format(data, result))
        client.send(struct.pack('I', result))


    def _send(self):
        self.__address = ('192.168.1.9', 7000)
        if self.__address is not None:
                message = 'hello'.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent

    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)

    def _clientslist(self):
        for client in clientslist['connectedclients']:
            print(client)
        return ''


class EchoClient():
    def __init__(self, host=socket.gethostname(), port=6000, message=None):
        self.__message = message
        self.__s = socket.socket()
        print('Écoute sur {}:{}'.format(host, port))
        self.__host = host
        self.__port = port

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send
        }
        if self.__message:
            self.__s.connect(SERVERADDRESS)
            self._send()
        self.__running = True
        self.__address = None
        param = ''
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ')+1:].rstrip()

            # Call the command handler
            if command in handlers:
                    handlers[command]() if param == '' else handlers[command](param)

            else:
                print('Command inconnue:', command)
        self.__s.close()

        # try:
        #     self.__s.connect((self.__host, self.__port))
        #     self._send(param)
        #     self.__s.close()
        # except OSError:
        #     print('Serveur introuvable, connexion impossible.')

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
                print('Connecté en tant que {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur lors de l'envoi du message.")

    def _send(self):
        totalsent = 0
        msg = self.__message
        try:
            while totalsent < len(msg):
                sent = self.__s.send(msg[totalsent:])
                totalsent += sent
        except OSError:
            print("Erreur lors de l'envoi du message.")

    def _receive(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(1024)
                print(data.decode())
            except socket.timeout:
                pass
            except OSError:
                return


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
                print('Command inconnue:', command)

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
    if len(sys.argv) == 4 and sys.argv[1] == 'server':
        SERVERADDRESS = (sys.argv[2], int(sys.argv[3]))
        EchoServer(sys.argv[2], int(sys.argv[3])).run()

    # elif len(sys.argv) == 4 and sys.argv[1] == 'client':
    #     EchoClient(sys.argv[2], int(sys.argv[3])).run()
    elif len(sys.argv) == 5 and sys.argv[1] == 'client':
        EchoClient(sys.argv[2], int(sys.argv[3]), sys.argv[4].encode()).run()
