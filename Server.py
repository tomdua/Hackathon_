import socket
import threading
import time
import struct
from random import randrange
import os
from _thread import *

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 2048
servserPort = 13117
global score_group1
global score_group2
global group1
global group2

# client_dic_a[ip] = (ip, score)
# client_dic_b[ip] = (ip, score)
score_group1 = 0
score_group2 = 0
group1 = []
group2 = []
 
def conn_tcp_theard():
    # Create a datagram socket
    TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # Bind to address and ip
    TCPServerSocket.bind((localIP, localPort))
    print("TCP server up and listening")
    TCPServerSocket.listen(10)

def shutdown_server(UDPServerSocket):
        ''' Shutdown the UDP server '''
        print('Shutting down server...')
        UDPServerSocket.close()
# def broadcast():
#     # while True:
#     #if start game or not
#     # host_name=socket.gethostname()
#     # ip=socket.gethostbyname(host_name)
#     # ip_name =client_address.encode()
#     # mes= "Server started, listening on IP address " + str(client_address)
#     # print(mes)
#     # resp='as'
#     # time_plus_10 = time.time() + 10
#     # while time.time() <= time_plus_10:
    
#     # UDPServerSocket.sendto(resp.encode('utf-8'), client_address)
#     # print('\n', resp, '\n')
#     # UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#     UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#     UDPServerSocket.bind((localIP, localPort))
#     UDPServerSocket.settimeout(0.2)
#     magic_cookie = 0xfeedbeef
#     message_type= 0x2
#     message = struct.pack('QQQ', magic_cookie, message_type,localPort)
#     while True:
#         UDPServerSocket.sendto(message, ('<broadcast>', 13117))
#         print('ms_sent')

# def wait_for_client():
#     ''' Wait for clients and handle their requests '''
#     UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#     UDPServerSocket.settimeout(10)
#     # Bind to address and ip
#     UDPServerSocket.bind((localIP, localPort))
#     print("UDP server up and listening")

#     clients=[]
#     t_end = time.time() + 10
#     try:
#         UDPServerSocket.settimeout(t_end - time.time())
#         while time.time() < t_end: # keep alive
#             try: # receive request from client
#                 data, client_address = UDPServerSocket.recvfrom(2024)
#                 c_thread = threading.Thread(target = broadcast,
#                                         args = (UDPServerSocket,data, client_address))
#                 c_thread.daemon = True
#                 c_thread.start()
#                 clients.append(client_address)
#                 rondom_team = randrange(2)
#                 if rondom_team % 2 == 0:
#                     group1.append(client_address)
#                 else:
#                     group2.append(client_address)
#             except OSError as err:
#                 print(err)
                
#     except KeyboardInterrupt:
#         print("Time is up for connecting new players")
#         shutdown_server(UDPServerSocket)
#     return clients,group1,group2

def start_tcp_server():
    print("starting game")
    message = "Welcome to Keyboard Spamming Battle Royale.\n"
    message += "Group 1:\n"
    message += "==\n"
    for client in group1:
        message += str(client)
    message += "Group 2:\n"
    message += "==\n"
    for client in group2:
        message += str(client)
    message += "Start pressing keys on your keyboard as fast as you can!!\n"
    return message
    # TCPServerSocket.connect(group1[0])
    # TCPServerSocket.sendall(message.encode())
def broadcast():
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDPServerSocket.bind((localIP, localPort))
    UDPServerSocket.settimeout(0.5)
    magic_cookie = 0xfeedbeef
    message_type= 0x2
    message = struct.pack('QQ', magic_cookie, message_type)
    time_plus_10=time.time()+10
    while time_plus_10>time.time():
        UDPServerSocket.sendto(message, ('<broadcast>',servserPort))
        print('Message_sent')
        time.sleep(1)

def multi_threaded_client(connection):
    groups = start_tcp_server()
    connection.send(str.encode('Server is working:'))
    connection.send(str.encode(groups))
    # data = connection.recv(2048)
    
   
 
    # time_plus_10 = time.time() + 10
    # while time.time() <= time_plus_10:
    while True:
        data = connection.recv(2048)
        # groups = start_tcp_server()
        # connection.sendall(str.encode(groups))
        msg ='Data From Client:' + data.decode('utf-8')
        response = 'Server message: Game over!' 
        if not data:
            break
        connection.sendall(str.encode(msg))
        connection.sendall(str.encode(response))
    connection.close()
 

def server():
    thread_udp = threading.Thread(target = broadcast,args = ())
    thread_udp.start()
    thread_tcp = threading.Thread(target=conn_tcp_theard(), args=())
    thread_tcp.start()

    ServerSideSocket = socket.socket()
    host = '127.0.0.1'
    # port = 2004
    port = 2001
    ThreadCount = 0
    try:
        ServerSideSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print('Socket is listening..')
    ServerSideSocket.listen(5)
    while True:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSideSocket.close()



    # thread_tcp = threading.Thread(target=conn_tcp_theard(), args=())
    # thread_tcp.start()
    # msgFromServer       = "Hello UDP Client"
    # bytesToSend         = str.encode(msgFromServer)
    # # Create a datagram socket
    # UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # # Enable broadcasting mode
    # UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind to address and ip
    # UDPServerSocket.bind((localIP, localPort))
    # print("UDP server up and listening")
    # Listen for incoming datagrams
    # while(True):
    #     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    #     message = bytesAddressPair[0]
    #     address = bytesAddressPair[1]
    #     clientMsg = "Message from Client:{}".format(message)
    #     clientIP  = "Client IP Address:{}".format(address)
    #     print(clientMsg)
    #     print(clientIP)
    #     # Sending a reply to client
    #     UDPServerSocket.sendto(bytesToSend, address)
   
   
    # # Set a timeout so the socket does not block
    # # indefinitely when trying to receive data.
    # UDPServerSocket.settimeout(10)
    # message = b"your very important message"
    # start_time = time.time()
    # while time.time() - start_time < 10:
    #     UDPServerSocket.sendto(message, ("127.0.0.1", 20001))
    #     print("message sent!")
    #     time.sleep(1)
    #     clients,group1,group2 = wait_for_client(UDPServerSocket)
    #     # UDPServerSocket.close()  
    # UDPServerSocket.close()


    # msgFromServer       = "Hello TCP Client"
    # bytesToSend         = str.encode(msgFromServer)
    # # Create a datagram socket
    # TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # # Bind to address and ip
    # TCPServerSocket.bind((localIP, localPort))
    # print("TCP server up and listening")
    #     # # start_tcp_server(TCPServerSocket,group1,group2)


if __name__ == "__main__":
    server()