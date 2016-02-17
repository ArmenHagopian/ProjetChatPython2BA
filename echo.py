<<<<<<< HEAD

=======
#!/usr/bin/env python3
# echo.py
# author: Sébastien Combéfis
# version: February 15, 2016
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0

import socket
import sys

SERVERADDRESS = (socket.gethostname(), 6000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
<<<<<<< HEAD

=======
        
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                print(self._receive(client).decode())
                client.close()
            except OSError:
                print('Erreur lors de la réception du message.')
<<<<<<< HEAD

=======
    
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)


class EchoClient():
    def __init__(self, message):
        self.__message = message
        self.__s = socket.socket()
<<<<<<< HEAD

=======
    
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
    def run(self):
        try:
            self.__s.connect(SERVERADDRESS)
            self._send()
            self.__s.close()
        except OSError:
            print('Serveur introuvable, connexion impossible.')
<<<<<<< HEAD

=======
    
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
    def _send(self):
        totalsent = 0
        msg = self.__message
        try:
            while totalsent < len(msg):
                sent = self.__s.send(msg[totalsent:])
                totalsent += sent
        except OSError:
            print("Erreur lors de l'envoi du message.")

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        EchoServer().run()
    elif len(sys.argv) == 3 and sys.argv[1] == 'client':
        EchoClient(sys.argv[2].encode()).run()