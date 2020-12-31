from colors import colors
import socket
import time
import signal, os
import sys, select
import getpass
import ssl
from threading import Timer
from threading import Thread
import struct
from random import randrange
import time
global finish_game
finish_game = False

def keyboard_event_handler(tcp_socket):
    """
    part of game mode - collect characters and from the keyboard and send them over TCP. collect
    data from the network. Input input - typing from the customer
    """
    try:
        with Input(keynames='curses') as input_generator:
            e = input_generator.send(10)
            future = time.time() + 10
            while e is not None:
                if finish_game:
                    break 
                tcp_socket.send(bytes(e, 'utf-8'))
                curr = future - time.time()
                e = input_generator.send(curr)
                
    except KeyboardInterrupt as e:
        raise KeyboardInterrupt("Interaption.")



def client():
    """
    Our main method in which we open connections in front of the server
    """
    msgFromClient       = "Hello UDP Server"
    # bytesToSend         = str.encode(msgFromClient)
    # serverAddressPort   = ("127.0.0.1", 20001)
    bufferSize          = 2048
    serverPort          = 13117
    serverTCPPort       = 11117

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Client started, listening for offer requests...")
    #GET server using created UDP socket
    ixd=randrange(255)
    UDPClientSocket.bind(("127.0.0.{}".format(ixd), serverPort))
    message, clientAddress = UDPClientSocket.recvfrom(bufferSize)
    print(struct.unpack('QQ',message))
    print("Message from Server: %s"%message)
    address = struct.unpack('QQ',message)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((clientAddress[0], serverTCPPort))
    tcp_socket.send("Yalla Hiafa.{}".format(ixd).encode("utf-8"))

    server_listen_text = tcp_socket.recv(bufferSize)
    open_client_text = tcp_socket.recv(bufferSize)

    # pass
    time_plus_10 = time.time() + 10
    while time.time() < time_plus_10:  # wait for input
        pass
        
    print(server_listen_text.decode('utf-8'))
    print(open_client_text.decode('utf-8'))
    # print ('You have 10 seconds to type in your stuff...')
    tcp_socket.sendall(b"a")
    
    # keyboard_event_handler(tcp_socket) - not work becsue the server

if __name__ == "__main__":
    client()
