import socket
import numpy as np 

UDP_IP = "127.0.0.1"
UDP_PORTS = np.arange(1000)+5000
MESSAGE = "Hello, World!"

sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP

for UDP_PORT in UDP_PORTS:
    print(UDP_PORT) 
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))