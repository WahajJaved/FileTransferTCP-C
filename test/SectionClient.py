#!/usr/bin/env python3

import sys,errno
import math
import socket
import random
import hashlib
import datetime
import time

SIZE_1_KiB = 1024
SIZE_32_KiB = 32 * SIZE_1_KiB


def md5(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()

def checkHash(section,hash):
    return (md5(section) == hash)
        

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     

    # # Define the port on which you want to connect 
    port = 7037                
    
    # connect to the server on local computer 
    client_socket.connect(('127.0.0.1', port)) 
    client_socket.sendall(b'LIST')
    
    data = []
    data = client_socket.recv(SIZE_32_KiB)
    data = data.decode()
    data = data.split("\n")

    client_socket.close()

    fileHash = data[0]
    data = data[1:]

    totalSections = len(data)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
    s.connect(('127.0.0.1', port)) 
    
    file = bytes()
    index = 0
    while True:
        
        
        dataObj = data[index]
        dataObj = dataObj.split()
        index = int(dataObj[0])
        size = int(dataObj[1])
        md5Hash = dataObj[2]

        text = 'SECTION '+ str(index)
        text = text.encode()  

        try:
            s.send(text)

        except:
            print("Connection Disrupted, ARetrying")
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
            s.connect(('127.0.0.1', port))
             
        
        section = s.recv(size)
           
        if (checkHash(section,md5Hash)):
            print("Section "+ dataObj[0]+" Downloaded Successfully")
            index+=1
            file += section
        else:
            print("Section "+ dataObj[0]+ " is corrupted, downloading again")

        if (index == totalSections):
            break

    if (checkHash(file,fileHash)):
        print("File Downloaded Successfully")

if __name__ == "__main__":
    sys.exit(main())