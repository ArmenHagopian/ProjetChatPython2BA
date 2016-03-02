# ProjetChatPython2BA
This is a chat application. It allows to connect to a server which communicates to the client all the connected ones. Then the client can start a peer-to-peer chat with one person of the list.

#Tutorial
To run the app, open the Terminal (OSX) or the Command Prompt (Windows). Run the adder.py programm with python3 and other parameters depending on the kind of chat you want to choose.
To connect the server, you can run adder.py in the Terminal like this : "python3 adder.py server"
To connect a client to the server, you can run adder.py in the Terminal like this : "python3 adder.py client ECAM 249.141.3.5 8000".The second argument is "server" and the last two elements are the IP address and the port you want to use.
Warning : You must give a password as third argument to access to the connected clients list, in this case the password is ECAM, you can easily change it in the file.
To start a peer-to-peer chat, you can run adder.py in the Terminal like this : python3 adder.py peer 249.141.3.5 7000. The second argument is "peer" and the last two elements are the IP address and the port you want to use.
To be able to communicate with others, 4 functions are implemented in the class 'chat()'.
The function '_join(self,param)' enable us to join someone who's connected to the server.
the function '_send(self)' enable us to send data towards a machine.
The function '_quit(self)' enable us to exit a peer to peer connection.
The function '_exit(self)' enable us to exit the program.

#Communication Protocols

UDP (User Datagram Protocol) protocol for the peer-to-peer communication and TCP (Transmission Control Protocol) protocol for the client/server one.

#Tests
All the programs have been tested on OSX Lion and El Capitan with python 3.
