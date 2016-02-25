import socket
import sys
import threading
import struct
import pickle


# faire en sort d'avoir le mm serveur pour EchoServer et EchoClient

SERVERADDRESS = (socket.gethostname(), 6000)
clientslist = dict()
clientslist["connectedclients"] = dict()


class EchoServer():
    def __init__(self, host=socket.gethostname(), port=6000):
        self.__s = socket.socket()
        self.__s.bind((host, port))
        self.__host = host
        self.__port = port

    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            print(addr)
            print(self._receive(client).decode())
            print(self._send())


    def _send(self):
        self.__address = (self.__host, 7000)
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
        s = socket.socket()
        s.settimeout(0.5)
        self.__s = s
        print('Écoute sur {}:{}'.format(host, port))
        self.__host = host
        self.__port = port

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send_peer
        }
        if self.__message:
            self.__s.connect((self.__host, self.__port))
            self._send_server()
            self.__s.close()
        self.__running = True
        self.__address = None
        threading.Thread(target=self._receive).start()
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

    def _send_peer(self, param):
        if self.__address is not None:
            try:
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
            except OSError:
                print('Erreur lors de la réception du message.')

    def _send_server(self):
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


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == 'server':
        EchoServer(sys.argv[2], int(sys.argv[3])).run()
        # SERVERADDRESS = (socket.gethostname(), 6000)

    # elif len(sys.argv) == 4 and sys.argv[1] == 'client':
    #     EchoClient(sys.argv[2], int(sys.argv[3])).run()
    elif len(sys.argv) == 5 and sys.argv[1] == 'client':
        EchoClient(sys.argv[2], int(sys.argv[3]), sys.argv[4].encode()).run()
