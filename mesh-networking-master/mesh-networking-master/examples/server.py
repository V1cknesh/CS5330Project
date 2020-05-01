import socket
import numpy as np 


UDP_IP = "127.0.0.1"
UDP_PORTS = np.arange(1000)+5000
sockets = []
for UDP_PORT in UDP_PORTS:
    try:
        print(UDP_PORT) 
        sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP

        sock.bind((UDP_IP, UDP_PORT))
        sockets.append(sock)
    except:
        continue

while True:
    for sock in sockets:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message:", data)