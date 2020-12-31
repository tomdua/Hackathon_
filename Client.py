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

bufferSize                  = 2048
serverPort                  = 13117
serverTCPPort               = 11117
SEC_10                      = 10
LOACL_IP                     = "127.0.0.1"
BIT_UNICODE_TRANSFORMATION  = 'utf-8'
TEAM_NAME                   = 'Yalla_Hiafa'

def keyboard_event_handler(tcp_socket):
    """ part of game mode - collect characters and from the keyboard and send them over TCP. collect
    data from the network. Input input - typing from the customer
    Args:
        tcp_socket (CONNECT): tcp connect socket

    Raises:
        KeyboardInterrupt
   """
    try:
        with Input(keynames='curses') as input_generator:
            e = input_generator.send(SEC_10)
            future = time.time() + SEC_10
            while e is not None:
                if finish_game:
                    break 
                tcp_socket.send(bytes(e, BIT_UNICODE_TRANSFORMATION))
                curr = future - time.time()
                e = input_generator.send(curr)
                
    except KeyboardInterrupt as e:
        raise KeyboardInterrupt("Interaption.")
        print("fail in getting tuch func")


def client():
    """
    Our main method in which we open connections in front of the server
    """

    # Create a UDP socket at client side
    #the UDP server which sends offers for 10 sec and connect all the clients that respond to those offers
    try:
        UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Client started, listening for offer requests...")
        #GET server using created UDP socket
        random_prefix=randrange(255)
        UDPClientSocket.bind((LOACL_IP+str(random_prefix), serverPort))
        message, clientAddress = UDPClientSocket.recvfrom(bufferSize)
        # print(struct.unpack('QQ',message))
        # print("Message from Server: %s"%message)

        address = struct.unpack('QQ',message)
    except Exception as e:
        print(e)

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((clientAddress[0], serverTCPPort))
    tcp_socket.send((TEAM_NAME+str(random_prefix)).encode(BIT_UNICODE_TRANSFORMATION))

    server_listen_text = tcp_socket.recv(bufferSize)
    open_client_text = tcp_socket.recv(bufferSize)
    end_client_text = tcp_socket.recv(bufferSize)
    
    # start game
    time_plus_10 = time.time() + SEC_10
    while time.time() < time_plus_10:  # wait for input
        time.sleep(1)
        pass   
    print(colors.BOLD+server_listen_text.decode(BIT_UNICODE_TRANSFORMATION))
    print(colors.OKGREEN+open_client_text.decode(BIT_UNICODE_TRANSFORMATION))
    print(colors.F_LightYellow+end_client_text.decode(BIT_UNICODE_TRANSFORMATION))
    
    # keyboard_event_handler(tcp_socket) - not work becsue the server

if __name__ == "__main__":
    client()
