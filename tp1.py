import socket
import time
import datetime
import json
localIP     = "192.168.1.40"##"10.145.16.75"
localPort   = 3000
Portmachine   = 4200
bufferSize  = 1024
msgFromServer  = "120"
bytesToSend =  bytes.fromhex("12")


# Opening JSON file
def openconfigfile():
    f = open('config.json')
    data = json.load(f)
    stringjson = data["strings"]["chooseDrinkText"]
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

def sendto(UDPServerSocket):
    UDPServerSocket.sendto(bytesToSend, (localIP, 4200))

def recerivefrom(UDPServerSocket):
    print("UDP server up and listening")
    # Listen for incoming datagrams
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    return bytesAddressPair

def decode(bytesAddressPair,stringjson):
    print(datetime.datetime.fromtimestamp(time.time()),bytesAddressPair[0])
    split1 = bytesAddressPair[0][:1]
    split2 = bytesAddressPair[0][1:2]
    split3 = bytesAddressPair[0][2:]
    stringresult = split3.decode("utf-8") 
    decode = int.from_bytes(split2, "big")    
    print(stringresult)
    print(split1,split2,split3,decode)
    if stringresult.__eq__(stringjson):
        print('aucune boisson n\'a été selectionnée et aucun prix n\'est affiché')
    else:
        print('une boisson est peut etre selectionné')   




if __name__ == "__main__":
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    sendto(UDPServerSocket)
    bytesAddressPair =recerivefrom(UDPServerSocket)
    stringjson = openconfigfile()
    decode(bytesAddressPair,stringjson)



 












