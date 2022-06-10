import socket
import time
import datetime
import json
localIP     = "10.30.5.10"
localPort   = 3000
Portmachine   = 4200
bufferSize  = 1024
msgFromServer  = "120"



# Opening JSON file
def openconfigfile():
    f = open('config.json')
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
    return codereturn


def checkIfCanSelectSuggar(bytesAddressPair,drinkselected):
    print(bytesAddressPair[0])
    codesuggar = bytesAddressPair[0][1:2]
    stringresult = codesuggar.decode("utf-8")     
    codesuggar =int.from_bytes(codesuggar, "big")
    if drinkselected == 1 and codesuggar == 0:
        print("une boisson a été selectionné et le nombre d'unités de sucre n'ai pas autorisé")
        return True
    elif  drinkselected == 1 and codesuggar == 1: 
        print("la boisson  a été selectionné et le sucre ne depasse pas 10 unités")
        return False
    else:
        print("il se peut que la boisson n'a pas ete valisdé")
        return False
        



## 02 latté | 01 italiano  | 03 cappucino | 04 good caffe | 05 Earl grey
## 06 green tea | 07 black tea | 08 soap | 00 americano


if __name__ == "__main__":
    first =  bytes.fromhex("2101")
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    #####################################first drink
    ## check if a drink is selected
    sendto(UDPServerSocket,first)
    bytesAddressPair =recerivefrom(UDPServerSocket)
    validatedrink = checkIfCanSelectDrink(bytesAddressPair) 
    ### check if possible to select suggar
    sendto(UDPServerSocket,bytes.fromhex("22-1"))
    validatesuggar =recerivefrom(UDPServerSocket)
    checkIfCanSelectSuggar(validatesuggar,validatedrink) 
