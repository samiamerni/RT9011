import socket
import time
import datetime
import json
localIP     = "10.188.168.50"
localPort   = 3000
Portmachine   = 4200
bufferSize  = 1024
msgFromServer  = "120"



def initializeUT(UDPServerSocket):
    print("initialisagion de UT")
    successut = 1 
    UDPServerSocket.sendto(bytes.fromhex("00"), (localIP, 4200))
    try:
        returnUT = UDPServerSocket.recvfrom(bufferSize)
    except socket.timeout:
        initverdic="inconc"
        return initverdic

    code = returnUT[0][1:2]
    if successut.__eq__(int.from_bytes(code, "big")) :
        print("initialisation UT reussite")
        initsucess="success"
        initverdic="pass"
        return initsucess
    else:
        print("initialisation UT echoué")        
        initfail="erreur"
        initverdic="fail"
        return initfail

def recerivefrom(UDPServerSocket):
    print("UDP server up and listening")
    # Listen for incoming datagrams
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    except socket.timeout:
        initverdic="inconc"
        return initverdic
    return bytesAddressPair


def initiateDatagram():
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    return UDPServerSocket

def sendto(UDPServerSocket,bytesToSend):
    UDPServerSocket.sendto(bytesToSend, (localIP, 4200))



def checkIfCanSelectDrink(bytesAddressPair):
    print(bytesAddressPair[0])
    codereturn = bytesAddressPair[0][1:2]
    stringresult = codereturn.decode("utf-8")     
    codereturn =int.from_bytes(codereturn, "big")
    if codereturn == 1:
        print("une boisson a été selectionnée")
        return True
    else:
        print("la boisson n'a pas ete selectionée")
        return False

def checkGetDrink(bytesAddressPair):
    print(bytesAddressPair[0])
    codemonnaie = bytesAddressPair[0][1:2]   
    codemonnaie =int.from_bytes(codemonnaie, "big")
    if codemonnaie == 1:
        print("la boisson a été recuperé")
        return False
    else:
        print("la boisson ne peut pas etre recuperere")
        return True
    
### tant qu'une boisson n'est validée, il n'est pas possible dde recuperer le rendu monnaie 


## 02 latté | 01 italiano  | 03 cappucino | 04 good caffe | 05 Earl grey
## 06 green tea | 07 black tea | 08 soap | 00 americano


if __name__ == "__main__":
    first =  bytes.fromhex("2100")
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    
    ## selectionner une boisson
    sendto(UDPServerSocket,first)
    bytesAddressPair =recerivefrom(UDPServerSocket)
    selectdrink = checkIfCanSelectDrink(bytesAddressPair) 
    ## recuperer boisson
    sendto(UDPServerSocket,bytes.fromhex("25"))
    getdrink =recerivefrom(UDPServerSocket)
    codeGetDrink=  checkGetDrink(getdrink)
