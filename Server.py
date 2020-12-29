import socket
import threading
import time
import struct

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
 
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
    # resp='as'
    # UDPServerSocket.sendto(resp.encode('utf-8'), client_address)
    # print('\n', resp, '\n')

    magic_cookie = 0xfeedbeef
    message_type= 0x02
    message = struct.pack('bbb', magic_cookie, message_type,localPort)
    time_plus_10 = time.time() + 10
    while time.time() <= time_plus_10:
        UDPServerSocket.sendto(message, (client_address, localPort))
        time.sleep(1)

def wait_for_client(UDPServerSocket):
    ''' Wait for clients and handle their requests '''
    clients=[]
    try:
        while True: # keep alive
            try: # receive request from client
                data, client_address = UDPServerSocket.recvfrom(1024)
                c_thread = threading.Thread(target = broadcast,
                                        args = (UDPServerSocket,data, client_address))
                c_thread.daemon = True
                c_thread.start()
            except OSError as err:
                print(err)
    except KeyboardInterrupt:
        shutdown_server(UDPServerSocket)
    return clients

# def start_tcp_server(TCPServerSocket):
#     TCPServerSocket.lis

 
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
    wait_for_client(UDPServerSocket)

    # start_time = time.time()
    # while time.time() - start_time < 10:
    #     UDPServerSocket.close()


    # msgFromServer       = "Hello TCP Client"
    # bytesToSend         = str.encode(msgFromServer)
    # # Create a datagram socket
    # TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # # Bind to address and ip
    # TCPServerSocket.bind((localIP, localPort))
    # print("TCP server up and listening")
    # # start_tcp_server(TCPServerSocket)

if __name__ == "__main__":
    server()