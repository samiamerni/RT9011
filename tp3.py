import socket
import time
import datetime
import json
localIP     = "192.168.1.40"
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

def decodeprice(bytesAddressPair,drinkSelected,stringjson):
    print(bytesAddressPair[0])
    price = bytesAddressPair[0][2:]
    stringresult = price.decode("utf-8")     
    print(stringresult)
    if stringjson["changeText"] == stringresult or stringjson["chooseDrinkText"] == stringresult or stringjson["drinkMadeText"] == stringresult or stringjson["noBucket"] == stringresult :
        print('le prix n\'est pas affiché')
        print('test echoué')
        return False
    else:
        print('le prix de la boisson est :',stringresult)
        print('test reussi') 
        return True

def decodeDrinkSelected(bytesAddressPair):
    print(datetime.datetime.fromtimestamp(time.time()),bytesAddressPair[0])
    coderesult = bytesAddressPair[0][1:2]
    coderesult = int.from_bytes(coderesult, "big")    
    if coderesult == 1 :
        print('une boisson a été selectionnée')
        return True
    else:
        print('aucune boisson n\'a été selectionnée')   
        return False


## 02 latté | 01 italiano  | 03 cappucino | 04 good caffe | 05 Earl grey
## 06 green tea | 07 black tea | 08 soap | 00 americano


if __name__ == "__main__":
    bytesToSend =  bytes.fromhex("2100")
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    ## check if a drink is selected
    sendto(UDPServerSocket,bytesToSend)
    bytesAddressPair =recerivefrom(UDPServerSocket)
    drinkSelected =decodeDrinkSelected(bytesAddressPair)
    ### check if price is printed
    sendto(UDPServerSocket,bytes.fromhex("12"))
    validatedrink =recerivefrom(UDPServerSocket)
    stringjson = openconfigfile()
    decodeprice(validatedrink,drinkSelected,stringjson)
    



 












