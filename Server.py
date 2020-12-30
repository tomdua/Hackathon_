from colors import colors
import socket
import threading
import time
import struct
from random import randrange
from threading import Thread

localIP                     = "127.0.0.1"
localPort                   = 20001
bufferSize                  = 2048
servserPort                 = 13117
tcpPort                     = 11117
SEC_10                      = 10
BIT_UNICODE_TRANSFORMATION  = 'utf-8'

global connection_client_dic
global score_group1
global score_group2
global group1
global group2

lock=threading.Lock()
score_group1 = 14
score_group2 = 20
group1 = {}
group2 = {}
connection_client_dic={}
global namesA
global namesB
namesA=[]
namesB=[]

global answer
answer = True


def keybord():
    """
    handel keybord clik
    : not check yet on server becuse its all the time diesconect
    """
    for sock in group1.values():
        threading.Thread(target=count_massage, args=(sock[1])).start()
    for sock in group2.values():
        threading.Thread(target=count_massage, args=(sock[1])).start()
    answer = False

def count_massage(sock):
    """
    count click massages
    """
    while answer:
        m = sock[1].recv(bufferSize)
        score_group1['a'] += 1

def shutdown_server(UDPServerSocket,TCPServerSocket):
    """
    Shutdown the UDP and TCP server
    #params - UDPServerSocket connction and TCPServerSocket connction
    """
    UDPServerSocket.close()
    TCPServerSocket.close()

def random_teams(client_keys):
    """
    split teams to 2 teams, and inster to list of names
    """
    rondom_team = randrange(20)
    conn = connection_client_dic[client_keys][0]
    port = connection_client_dic[client_keys][1]
    if rondom_team % 2 == 0:
        group1[client_keys]=(port,conn)
        namesA.append(client_keys+'\n')
    else:
        group2[client_keys]=(port,conn)
        namesB.append(client_keys+'\n')


def generate_end_message():
    """
    create and send to all clients the end message
    @return -  byte message

    """
    countA = 10
    countB = 20
    end_message = "\nGame over!\nGroup 1 typed in " + str(countA) + " characters. Group 2 typed in " + str(countB) + " characters.\n"
    if countA > countB:
        end_message += "\nGroup 1 wins!\nCongratulations to the winners:\n==\n"
        for client in namesA:
            end_message += str(client)
    elif countB > countA:
        end_message += "\nGroup 2 wins!\nCongratulations to the winners:\n==\n"
        for client in namesB:
            end_message += str(client)
    else:
        end_message += "\nDraw!\nCongratulations to the winners:\n==\n"
        for client in namesA:
            end_message += str(client)
        for client in namesB:
            end_message += str(client)
    end_message += "\nGame Over\n==\n"
    return end_message

def generate_start_message():
    """
    create and send to all clients the start(welcome) message
    @return -  byte message

    """
    message = "Welcome to Keyboard Spamming Battle Royale.\n"
    message += "Group 1:\n"
    message += "==\n"
    for client in namesA:
        message += str(client)
    message += "\nGroup 2:\n"
    message += "==\n" 
    for client in namesB:
        message += str(client)
    message += "\nStart pressing keys on your keyboard as fast as you can!!\n"
    return message
    

def start_game():
    """
    start the clients game
    call the split function, keybord listner
    """
    count=0
    for client_keys in connection_client_dic.keys():
        random_teams(client_keys)
    begin_message= generate_start_message()
    begin_message=begin_message.encode()
    
    end_message= generate_end_message()
    end_message= end_message.encode()
    for client_keys in connection_client_dic.values():
        client_keys[0].send(begin_message)
        client_keys[0].send(end_message)

    # for client_keys in connection_client_dic.values():
    #      count+=client_keys[0].recv(bufferSize).decode()

    # x = threading.Thread(target=keybord, args=())
    # x.start()
    time_plus_10 = time.time()+SEC_10
    while time.time()<time_plus_10:
        time.sleep(1)
        pass

def broadcast():
    """
    send a broadcast massages on udp prtocol (use udp socket)
    use struct package
    """
    try:
        UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        UDPServerSocket.bind((localIP, localPort))
        message = colors.OKCYAN+"Server started, listening on IP address " + localIP
        print(message)
        UDPServerSocket.settimeout(0.5)
        magic_cookie = 0xfeedbeef
        message_type= 0x2
        message = struct.pack('QQ', magic_cookie, message_type)
        time_plus_10=time.time()+SEC_10
        while time_plus_10>time.time():
            UDPServerSocket.sendto(message, ('<broadcast>',servserPort))
            # print('Message_sent')
            time.sleep(1)
    except Exception as e:
        UDPServerSocket.close()
        print(e)


def connect_clients(tcp_connect):
    """
    connect to all clients on tcp protcol
    @param - a tcp connection from the start server
    """
    try:            
        time_plus_10 = time.time() + SEC_10
        tcp_connect.settimeout(time_plus_10 - time.time())
        while True:
            conn, client_address = tcp_connect.accept()
            data = conn.recv(bufferSize)
            thread_team_name = data.decode(BIT_UNICODE_TRANSFORMATION)
            lock.acquire()
            connection_client_dic[thread_team_name] = conn,client_address
            print("New player connected")
            lock.release()
    except Exception as e:
        print(e)

def start_server():
    """
    Our main method in which we open connections 
    """
    try:
        # Create a datagram socket
        try:
            TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Bind to address and ip
            TCPServerSocket.bind((localIP, tcpPort))
            print("TCP server up and listening")
            TCPServerSocket.listen(SEC_10)
        except Exception as e:
            print(e)

        connection_client_dic={}
        thread_udp = Thread(target = broadcast,args = ())
        thread_tcp = Thread(target = connect_clients,args=(TCPServerSocket,))

        thread_udp.start()
        thread_tcp.start()
        thread_udp.join()
        thread_tcp.join()
        start_game()
        shutdown_server(TCPServerSocket,TCPServerSocket)
    except EOFError as error:
        print(error)

    

if __name__ == "__main__":
    start_server()
