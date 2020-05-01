#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import _thread


def on_new_client(clientsocket, addr):
    while True:
        msg = clientsocket.recv(1024)
        # do some checks and if msg == someWeirdSignal: break:
        print(addr, ' >> ', msg)
        msg = input('SERVER >> ')
        # Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        clientsocket.send(msg.encode())
    clientsocket.close()


s = []
for i in range(0, 100):
    s.append(socket.socket())         # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 50000+i                # Reserve a port for your service.

    print('Server started!')
    print('Waiting for clients...')

    s[i].bind((host, port))        # Bind to the port
    s[i].listen(5)                 # Now wait for client connection.

while True:
    for i in range(0, 100):
        c, addr = s[i].accept()     # Establish connection with client.
        print('Got connection from', addr)
        _thread.start_new_thread(on_new_client, (c, addr))
        # Note it's (addr,) not (addr) because second parameter is a tuple
        # Edit: (c,addr)
        # that's how you pass arguments to functions when creating new threads using thread module.
   
for i in range(0, 100):     
    s[i].close()
