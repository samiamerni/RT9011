import socket
import time
import datetime
import json
localIP     = "10.188.168.50"
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
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    except socket.timeout:
        initverdic="inconc"
        return initverdic
    return bytesAddressPair

def printPriceOfSelectedDrink(bytesAddressPair):
    print(bytesAddressPair[0])
    price = bytesAddressPair[0][2:]
    stringresult = price.decode("utf-8")     
    print(stringresult)
    return stringresult


def compare(price1,price2):
     
    if price1 != price2 :
        print('le prix a ete modifié')
        print('test reussi')
        return True
    else:
        print('le prix n\'a pas eté modifié')   
        print('test echoué')
        return False


## 02 latté | 01 italiano  | 03 cappucino | 04 good caffe | 05 Earl grey
## 06 green tea | 07 black tea | 08 soap | 00 americano


if __name__ == "__main__":
    first =  bytes.fromhex("2100")
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    #####################################first drink
    ## check if a drink is selected
    sendto(UDPServerSocket,first)
    bytesAddressPair =recerivefrom(UDPServerSocket)
   
    ### check if price is printed
    sendto(UDPServerSocket,bytes.fromhex("12"))
    validatedrink =recerivefrom(UDPServerSocket)
    price1= printPriceOfSelectedDrink(validatedrink) 
    ##################################### Second drink
    ## check if a drink is selected
    second =  bytes.fromhex("2101")
    sendto(UDPServerSocket,second)
    bytesAddressPair =recerivefrom(UDPServerSocket)
    
    ### check if price is printed
    sendto(UDPServerSocket,bytes.fromhex("12"))
    validatedrink =recerivefrom(UDPServerSocket)
    price2 = printPriceOfSelectedDrink(validatedrink)

    ### comparer les deux prix
    compare(price2,price1)
    



 












