#!usr/bin/python
import hl7
import socket
from datetime import datetime
import requests,json

host = "172.20.20.67"
port = 7070
s = socket.socket()		# TCP socket object
s.connect((host,port))
k='This will be sent to server'
	
while (1):
    data = s.recv(2048)	
    #print("A")
   
    print(data)
    #print(data.decode())
    # close the connection
    
   