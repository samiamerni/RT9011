import socket
import datetime
import json
import time

localIP     = "10.188.168.50"
localPort   = 3000
Portmachine   = 4200
bufferSize  = 1024
msgFromServer  = "120"



# Opening JSON file
def openconfigfile():
    f = open('../config.json')
    data = json.load(f)
    stringjson = data["strings"]
    return stringjson

def initializeUT(UDPServerSocket):
    print("initialisagion de UT")
    successut = 1 
    UDPServerSocket.sendto(bytes.fromhex("00"), (localIP, 4200))
    returnUT = UDPServerSocket.recvfrom(bufferSize)
    code = returnUT[0][1:2]
    if successut.__eq__(int.from_bytes(code, "big")) :
        print("initialisation UT reussite")
    else:
        print("initialisation UT echoué")


def initiateDatagram():
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    return UDPServerSocket

def sendto(UDPServerSocket,bytesToSend):
    UDPServerSocket.sendto(bytesToSend, (localIP, 4200))

def recerivefrom(UDPServerSocket):
    print("UDP server up and listening")
    # Listen for incoming datagrams
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    return bytesAddressPair


def checkIfCanSelectDrink(bytesAddressPair):
    print(bytesAddressPair[0])
    codereturn = bytesAddressPair[0][1:2]
    stringresult = codereturn.decode("utf-8")     
    codereturn =int.from_bytes(codereturn, "big")
    if codereturn == 1:
        print("une boisson a été selectionnée alors qu'il n'ya plus de goblets")
        return False
    else:
        print("la boisson n'a pas ete selectionnée")
        return True


## 02 latté | 01 italiano  | 03 cappucino | 04 good caffe | 05 Earl grey
## 06 green tea | 07 black tea | 08 soap | 00 americano


if __name__ == "__main__":
    first =  bytes.fromhex("2108")
    ## renitiliaser UT
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    ## plus de boisson
    sendto(UDPServerSocket,bytes.fromhex("31"))
    #bytesAddressPair =recerivefrom(UDPServerSocket)
    #print(bytesAddressPair)
    ## selectionner une boisson
    time.sleep(5)
    sendto(UDPServerSocket,first)
    bytesAddressPair =recerivefrom(UDPServerSocket)
    selectdrink = checkIfCanSelectDrink(bytesAddressPair) 


