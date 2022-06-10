import socket
import time
import datetime
import json
localIP     = "192.168.1.40"##"10.145.16.75"
localPort   = 3000
Portmachine   = 4200
bufferSize  = 1024
msgFromServer  = "120"



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

def sendto(UDPServerSocket,bytesToSend):
    UDPServerSocket.sendto(bytesToSend, (localIP, 4200))

def recerivefrom(UDPServerSocket):
    print("UDP server up and listening")
    # Listen for incoming datagrams
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    return bytesAddressPair

def decodeselect(bytesAddressPair,stringjson):
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
        return False
    else:
        print('une boisson est peut etre selectionné')   
        return True

def decodevalidate(bytesAddressPair):
    print(datetime.datetime.fromtimestamp(time.time()),bytesAddressPair[0])
    coderesult = bytesAddressPair[0][1:2]
    coderesult = int.from_bytes(coderesult, "big")    
    if coderesult == 0 and  drinkSelected == False:
        print('aucune boisson n\'a été selectionnée et aucune boisson n\'a été validé ')
        print('test reussi')
    else:
        print('une boisson est peut etre validée')   
        print('test echoué') 




if __name__ == "__main__":
    bytesToSend =  bytes.fromhex("12")
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    ## check if a drink is selected
    sendto(UDPServerSocket,bytesToSend)
    bytesAddressPair =recerivefrom(UDPServerSocket)
    stringjson = openconfigfile()
    drinkSelected =decodeselect(bytesAddressPair,stringjson)
    ### check if we can validate drink
    sendto(UDPServerSocket,bytes.fromhex("23"))
    validatedrink =recerivefrom(UDPServerSocket)
    decodevalidate(validatedrink,drinkSelected)
    



 












