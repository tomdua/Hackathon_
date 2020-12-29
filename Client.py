import socket
import struct
from random import randrange

def client():
    msgFromClient       = "Hello UDP Server"
    bytesToSend         = str.encode(msgFromClient)
    serverAddressPort   = ("127.0.0.1", 20001)
    bufferSize          = 2048
    serverPort          = 13117


    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Client started, listening for offer requests...")
    #GETserver using created UDP socket
    ixd=randrange(255)
    UDPClientSocket.bind(("127.0.0.{}".format(ixd), serverPort))
    while True:
        message, clientAddress = UDPClientSocket.recvfrom(bufferSize)
        print(struct.unpack('QQ',message))
        print("Message from Server: %s"%message)
    UDPClientSocket.close()
    
    # msg = "Message from Server {}".format(msgFromServer[0])
    # print(msg)


if __name__ == "__main__":
    client()