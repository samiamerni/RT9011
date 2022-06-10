import socket
import time
import datetime
import json
localIP     = "10.192.50.77"
localPort   = 3000
Portmachine   = 4200
bufferSize  = 1024
msgFromServer  = "120"
bytesToSend =  bytes.fromhex("12")


# Opening JSON file
def openconfigfile():
    f = open('../config.json')
    data = json.load(f)
    stringjson = data["strings"]["chooseDrinkText"]
    return stringjson

def initializeUT(UDPServerSocket):
    print("initialisagion de UT")
    successut = 1  ### x01 en entier est 1   1 == succes 0 == echoue
    UDPServerSocket.sendto(bytes.fromhex("00"), (localIP, 4200))
    try:
        returnUT = UDPServerSocket.recvfrom(bufferSize)
    except socket.timeout:
        return "inconc"
    
    code = returnUT[0][1:2]
    if successut.__eq__(int.from_bytes(code, "big")) :
        print("initialisation UT reussite")
        return "success"
    else:
        print("initialisation UT echoué")
        return "fail"


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
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    except socket.timeout:
        return "inconc"
    return bytesAddressPair

def decode(bytesAddressPair,stringjson):
    print(datetime.datetime.fromtimestamp(time.time()),bytesAddressPair[0])
    code = bytesAddressPair[0][:1]
    lent = bytesAddressPair[0][1:2]
    split3 = bytesAddressPair[0][2:]
    stringresult = split3.decode("utf-8") 
    lent = int.from_bytes(lent, "big")  
    code = int.from_bytes(code, "big")  ### equivalent de x11 est 17 en entier   
    if stringresult.__eq__(stringjson) and code == 17 :
        print('aucune boisson n\'a été selectionnée et aucun prix n\'est affiché')
        return "sucess"
    else:
        print('une boisson est peut etre selectionné')   
        return "fail"


if __name__ == "__main__":
    UDPServerSocket = initiateDatagram()
    resultUT= initializeUT(UDPServerSocket)
    print("initialisateur:",resultUT)
    sendto(UDPServerSocket)
    bytesAddressPair =recerivefrom(UDPServerSocket)
    stringjson = openconfigfile()
    resultFinal= decode(bytesAddressPair,stringjson)
    print("resultat final",resultFinal)


 












