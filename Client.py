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
import time
import tty
from msvcrt import getch
answer = None
import 

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
            Thread(target = check).start()
            print ('You have 10 seconds to type in your stuff...')
            ans = getpass.getpass("Input something:")
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
    serverTCPPort       = 11117


    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Client started, listening for offer requests...")
    #GETserver using created UDP socket
    ixd=randrange(255)
    UDPClientSocket.bind(("127.0.0.{}".format(ixd), serverPort))
    message, clientAddress = UDPClientSocket.recvfrom(bufferSize)
    print(struct.unpack('QQ',message))
    print("Message from Server: %s"%message)
    address = struct.unpack('QQ',message)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((clientAddress[0], serverTCPPort))

    tcp_socket.send("Yalla Hiafa.{}".format(ixd).encode("utf-8"))

    # tcp_socket.sendall(str.encode('yalha hifa'))
    # tcp_socket.send(bytes('yalha hifa', encoding='utf8'))

    time_plus_10 = time.time() + 10
    print1=False
    # tcp_socket.settimeout(time_plus_10 - time.time())
    # while True:  # wait for input
    server_listen_text = tcp_socket.recv(1024)
    open_client_text = tcp_socket.recv(1024)
    # pass
    end = time.time() + 10
    while time.time() < end:  # wait for input
        pass

    print(server_listen_text.decode('utf-8'))
    print(open_client_text.decode('utf-8'))

    print ('You have 10 seconds to type in your stuff...')

    # settings=termios.tcgetattr(sys.stdin)
    # try:
    #     tty.setcbreak(sys.stdin.fileno())
    #     while True:
    #         readable, writable, exceptional = select.select([tcp_socket, sys.stdin],[],[],0)
    #         if tcp_socket in readable:
    #             try:
    #                 msg = tcp_socket.recv(bufferSize).decode()
    #             except ConnectionResetError:
    #                 break
    #             if msg:
    #                 print(msg)
    #                 break
    #         if sys.stdin in readable:
    #             try:
    #                 char = getch.getch()
    #             except OverflowError:
    #                 print('change key')
    #             try:
    #                 tcp_socket.send(char.encoded())
    #             except (BrokenPipeError,ConnectionResetError):
    #                 print('server close')
    #                 return
    # finally:
    #     termios



    s = getpass.getpass("Input something:")
    # print("Input something:")
    # from msvcrt import getch
    # time_plus_10 = time.time() + 10
    # while time.time()<time_plus_10:
    #     key = getch()
    # print(key)
    # s = input()
    # wait for time completion
    tcp_socket.send(str.encode(s))
    data_from_client_txet = tcp_socket.recv(1024)
    score_text = tcp_socket.recv(1024)
    finally_text = tcp_socket.recv(1024)
    print(data_from_client_txet.decode('utf-8'))
    print(score_text.decode('utf-8'))
    print(finally_text.decode('utf-8'))

    




if __name__ == "__main__":
    client()
