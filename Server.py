class colors:
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    F_White = "\x1b[97m"
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    HEADER = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    F_White = "\x1b[97m"
    F_LightYellow = "\x1b[93m"
    F_LightBlue = "\x1b[94m"
    F_LightMagenta = "\x1b[95m"

import socket
import threading
import time
import struct
from random import randrange
from threading import Thread
from _thread import start_new_thread

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 2048
servserPort = 13117
global connection_client_dic
global score_group1
global score_group2
global group1
global group2
global temp
temp=''
lock=threading.Lock()
score_group1 = 0
score_group2 = 0
group1 = {}
group2 = {}
connection_client_dic={}
global namesA
global namesB
namesA=[]
namesB=[]

def conn_tcp_theard():
    # Create a datagram socket
    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to address and ip
    TCPServerSocket.bind((localIP, localPort))
    print("TCP server up and listening")
    TCPServerSocket.listen(10)



def shutdown_server(UDPServerSocket):
        ''' Shutdown the UDP server '''
        print('Shutting down server...')
        UDPServerSocket.close()


def random_teams(client_keys):
    # print(type(connection_client_dic))
    # print(connection_client_dic[client_keys][1])
    rondom_team = randrange(20)
    conn = connection_client_dic[client_keys][0]
    port = connection_client_dic[client_keys][1]
    if rondom_team % 2 == 0:
        group1[client_keys]=(port,conn)
        namesA.append(client_keys+'\n')
        # print(namesA)
    else:
        group2[client_keys]=(port,conn)
        # namesB =+ str(client_keys)+'\n'
        namesB.append(client_keys+'\n')
        # print(namesB)
        
def generate_start_message():
    message = "Welcome to Keyboard Spamming Battle Royale.\n"
    message += "Group 1:\n"
    message += "==\n"
    # message += str(namesA)
    for client in namesA:
        message += str(client)
    message += "\nGroup 2:\n"
    message += "==\n" 
    # message += str(namesB)
    for client in namesB:
        message += str(client)
    message += "\nStart pressing keys on your keyboard as fast as you can!!\n"
    return message
    
def start_tcp_game():
    for client_keys in connection_client_dic.keys():
        random_teams(client_keys)
    begin_message= generate_start_message()
    begin_message=begin_message.encode()
    
    for client_keys in connection_client_dic.values():
        client_keys[0].send(begin_message)

    time_plus_10 = time.time()
    while time.time()<time_plus_10:
        pass
    for client_keys in group1.values():
        number = len((client_keys[0].recv(bufferSize).decode()))
        score_group1+=number
    for client_keys in group2.values():
        number = len((client_keys[0].recv(bufferSize).decode()))
        score_group2+=number


def broadcast():
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDPServerSocket.bind((localIP, localPort))
    message = colors.OKCYAN+"Server started, listening on IP address " + localIP
    print(message)
    UDPServerSocket.settimeout(0.5)
    magic_cookie = 0xfeedbeef
    message_type= 0x2
    message = struct.pack('QQ', magic_cookie, message_type)
    time_plus_10=time.time()+10
    while time_plus_10>time.time():
        UDPServerSocket.sendto(message, ('<broadcast>',servserPort))
        print('Message_sent')
        time.sleep(1)
    UDPServerSocket.close()


def connect_clients(tcp_connect):
    # tcp_connect.settimeout(time.time()+10 - time.time())
    try:            
        time_plus_10 = time.time() + 10
        tcp_connect.settimeout(time_plus_10 - time.time())
        while True:
            # while time.time() < time_plus_10:
            #     try:
                    # connection, client_address = tcp_connect.accept()
                    # res3 = tcp_connect.recv(bufferSize)
                    # print(res3.decode('utf-8'))
                    # TeamName = str(tcp_connect.recv(1024), 'utf-8')
                    # connection_client_dic[connection] = client_address
                    # print("New player connected")
                    # print(connection_client_dic[connection])
                # except:
                #     print("Time is up for connecting new players")
        # TeamName = str(TCPServerSocket.recv(1024), 'utf-8')
        # print(TeamName)
            conn, client_address = tcp_connect.accept()
            
            data = conn.recv(2048)
            thread_team_name = data.decode('utf-8')
            lock.acquire()
            #connection_client_dic[thread_team_name] = conn
            connection_client_dic[thread_team_name] = conn,client_address
            # start_new_thread(multi_threaded_client,(conn,))
            # time.sleep(10)
            print("New player connected")
            # print(connection_client_dic[thread_team_name])
            # print(conn)
            # start_new_thread(multi_threaded_client,(conn,))
            lock.release()
        tcp_connect.close()

    except:
        mes='time_up'


def generate_end_message():
    # countA = count_characters(group1)
    # countB = count_characters(group2)
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
    return end_message



def multi_threaded_client(connection):
    try:
        groups = start_tcp_game()
        connection.send(str.encode('Server is working:'))
        connection.send(str.encode(groups))
        data = connection.recv(bufferSize)
        # groups = start_tcp_server()
        # connection.sendall(str.encode(groups))
        dataString = data.decode('utf-8')
        msg ='Data From Client:' + dataString
        count = 'score of client:' + str(len(dataString))
        response = 'Server message:\n' + generate_end_message( 'nicole\nnicole','tom\ntom')
        # message.length()
        
        print(type(count))

        connection.send(str.encode(msg))
        connection.send(str.encode(count))
        connection.sendall(str.encode(response))

    except:
        print('hi')

def server():
    # tcp_connect=conn_tcp_theard
    # Create a datagram socket
    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to address and ip
    TCPServerSocket.bind((localIP, 11117))
    print("TCP server up and listening")
    TCPServerSocket.listen(10)

    connection_client_dic={}
    thread_udp = Thread(target = broadcast,args = ())
    thread_tcp = Thread(target = connect_clients,args=(TCPServerSocket,))
    # start_new_thread(multi_threaded_client,(temp.decode('utf-8'),))

    thread_udp.start()
    thread_tcp.start()
    thread_udp.join()
    thread_tcp.join()
    start_tcp_game()
    TCPServerSocket.close()

if __name__ == "__main__":
    server()
