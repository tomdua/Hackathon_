import socket
import time
import signal, os
import sys, select
import threading, msvcrt
import getpass
import ssl
from threading import Timer
from threading import Thread
import struct
from random import randrange
TIMEOUT = 10
answer = None

def check():
            # print ('You have 10 seconds to type in your stuff...')
            time.sleep(10)
            if answer != None:
                return 
            # print("Too Slow")

def input():
    try:
            # answer = input("Input something: ")
            # t = Timer(10, timeout)
            # t.start()
            print ('You have 10 seconds to type in your stuff...')
            Thread(target = check).start()
            ans = getpass.getpass("Input something:"+'\n')
            # t.join()
            # print(ans)
            return ans
    except:
            # timeout
            return "You said nothing!"

def client():
    msgFromClient       = "Hello UDP Server"
    bytesToSend         = str.encode(msgFromClient)
    serverAddressPort   = ("127.0.0.1", 20001)
    bufferSize          = 2048
    serverPort          = 13117


    # # Create a UDP socket at client side
    # UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # print("Client started, listening for offer requests...")
    # #GETserver using created UDP socket
    # ixd=randrange(255)
    # UDPClientSocket.bind(("127.0.0.{}".format(ixd), serverPort))
    # while True:
    #     message, clientAddress = UDPClientSocket.recvfrom(bufferSize)
    #     print(struct.unpack('QQ',message))
    #     print("Message from Server: %s"%message)
    # UDPClientSocket.close()
    
    # msg = "Message from Server {}".format(msgFromServer[0])
    # print(msg)

    # TCP
    ClientMultiSocket = socket.socket()
    host = '127.0.0.1'
    # port = 2004
    port = 2001

    print('Waiting for connection response')
    try:
        ClientMultiSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    res = ClientMultiSocket.recv(1024)
    resres = ClientMultiSocket.recv(1024)
    time_plus_10 = time.time() + 10
    if time.time() <= time_plus_10:
    # while True:
        print(res.decode('utf-8'))
        print(resres.decode('utf-8'))
        print('Start pressing keys on your keyboard as fast as you can!!')
        # Input = input('Start pressing keys on your keyboard as fast as you can!!')
        # duration is in seconds
        s = input()
        # wait for time completion

        ClientMultiSocket.send(str.encode(s))
        res1 = ClientMultiSocket.recv(1024)
        res2 = ClientMultiSocket.recv(1024)
        
        print(res1.decode('utf-8'))
        print(res2.decode('utf-8'))

    ClientMultiSocket.close()
if __name__ == "__main__":
    client()