<<<<<<< HEAD

=======
#!/usr/bin/env python3
# chat.py
# author: Sébastien Combéfis
# version: February 15, 2016
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0

import socket
import sys
import threading

class Chat():
<<<<<<< HEAD
    def __init__(self, host=socket.gethostname(), port=7000):
=======
    def __init__(self, host=socket.gethostname(), port=5000):
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, port))
        self.__s = s
        print('Écoute sur {}:{}'.format(host, port))
<<<<<<< HEAD

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send
=======
        
    def run(self):
        handlers = {
            'exit': self._exit,
            'quit': self._quit,
            'join': self._join,
            'send': self._send
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
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
<<<<<<< HEAD

=======
    
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()
<<<<<<< HEAD

    def _quit(self):
        self.__address = None

=======
    
    def _quit(self):
        self.__address = None
    
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
    def _join(self, param):
        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                self.__address = (tokens[0], int(tokens[1]))
                print('Connecté à {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur lors de l'envoi du message.")
<<<<<<< HEAD

=======
    
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
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
<<<<<<< HEAD

=======
    
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
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
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    else:
<<<<<<< HEAD
        Chat().run()
=======
        Chat().run()
>>>>>>> 7c3c9f64b9584d124829eae09039eb935524fbb0
