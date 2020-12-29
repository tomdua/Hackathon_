import socket
import threading
import time
import struct
from random import randrange

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 2048
 
def shutdown_server(UDPServerSocket):
        ''' Shutdown the UDP server '''
        print('Shutting down server...')
        UDPServerSocket.close()

def broadcast(UDPServerSocket,data, client_address):
    # while True:
    #if start game or not
    # host_name=socket.gethostname()
    # ip=socket.gethostbyname(host_name)
    # ip_name =client_address.encode()
    mes= "Server started, listening on IP address " + str(client_address)
    print(mes)
    resp='as'
    # time_plus_10 = time.time() + 10
    # while time.time() <= time_plus_10:
    # UDPServerSocket.sendto(resp.encode('utf-8'), client_address)
    # print('\n', resp, '\n')
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    magic_cookie = 0xfeedbeef
    message_type= 0x2
    message = struct.pack('QQQ', magic_cookie, message_type,localPort)
    # time_plus_10 = time.time() + 10
    # while time.time() <= time_plus_10:
    UDPServerSocket.sendto(message, ("255.255.255.255", 54549))
    time.sleep(1)

def wait_for_client(UDPServerSocket):
    ''' Wait for clients and handle their requests '''
    clients=[]
    group1=[]
    group2=[]
    t_end = time.time() + 10
    UDPServerSocket.settimeout(t_end - time.time())
    try:
        while time.time() < t_end: # keep alive
            try: # receive request from client
                data, client_address = UDPServerSocket.recvfrom(1024)
                c_thread = threading.Thread(target = broadcast,
                                        args = (UDPServerSocket,data, client_address))
                c_thread.daemon = True
                c_thread.start()
                clients.append(client_address)
                rondom_team = randrange(2)
                if rondom_team % 2 == 0:
                    group1.append(client_address)
                else:
                    group2.append(client_address)
            except OSError as err:
                print(err)
    except KeyboardInterrupt:
        print("Time is up for connecting new players")
        shutdown_server(UDPServerSocket)
    return clients,group1,group2


def start_tcp_server(TCPServerSocket,group1,group2):
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
    print(message)
    # TCPServerSocket.connect(group1[0])
    # TCPServerSocket.sendall(message.encode())


 
def server():
    msgFromServer       = "Hello UDP Client"
    bytesToSend         = str.encode(msgFromServer)
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")
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
    clients,group1,group2 = wait_for_client(UDPServerSocket)
    UDPServerSocket.close()
    # start_time = time.time()
    # while time.time() - start_time < 10:
    #     UDPServerSocket.close()


    msgFromServer       = "Hello TCP Client"
    bytesToSend         = str.encode(msgFromServer)
    # Create a datagram socket
    TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # Bind to address and ip
    TCPServerSocket.bind((localIP, localPort))
    print("TCP server up and listening")
    start_tcp_server(TCPServerSocket,group1,group2)


if __name__ == "__main__":
    server()