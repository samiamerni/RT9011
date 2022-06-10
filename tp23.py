import socket
import time
import datetime
import json
localIP     = "10.192.50.77"
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


def checkIfValidateDrink(bytesAddressPair):
    print(bytesAddressPair[0])
    codedrink = bytesAddressPair[0][1:2]
    #stringresult = codedrink.decode("utf-8")     
    codedrink =int.from_bytes(codedrink, "big")
    if codedrink == 1:
        print("une boisson a été validé")
        return True
    else:
        print("la boisson n'a pas ete validé")
        return False

def checkIfMonnaieInserted(bytesAddressPair):
    print(bytesAddressPair[0])
    codemonnaie = bytesAddressPair[0][1:2]
    #stringresult = codedrink.decode("utf-8")     
    codemonnaie =int.from_bytes(codemonnaie, "big")
    if codemonnaie == 1:
        print("les pieces sont insérés")
        return True
    else:
        print("les pieces ne sont pas inserer")
        return False

def checkGetMonnaie(bytesAddressPair):
    print(bytesAddressPair[0])
    codemonnaie = bytesAddressPair[0][1:2]   
    codemonnaie =int.from_bytes(codemonnaie, "big")
    if codemonnaie == 1:
        print("les pieces sont recupérés")
        return True
    else:
        print("les pieces ne sont pas recupérés, vous devez d'abord payer la totalité")
        return False


def compare(codedrink,codemonnaie):
    if codedrink == True and codemonnaie == True:
        print("la boisson a été validé et les pieces ont eté inserer")
        return True
    elif codedrink == False and codemonnaie == True:
        print("la boisson n'a pas été validé")
        return False
    else:
        print("la boisson n'a été validé ou les pieces n'ont pas ete inserer")
        return False

def checkIfCantSelectDrink(bytesAddressPair):
    print(bytesAddressPair[0])
    codereturn = bytesAddressPair[0][1:2]
    stringresult = codereturn.decode("utf-8")     
    codereturn =int.from_bytes(codereturn, "big")
    if codereturn == 1:
        print("une boisson a été selectionnée")
        return False
    else:
        print("la boisson n'a pas ete selectionée vous devriez reprendre la monnaie d'abord")
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
    ### valider la boisson
    sendto(UDPServerSocket,bytes.fromhex("2300"))
    validatedrink =recerivefrom(UDPServerSocket)
    codedrink = checkIfValidateDrink(validatedrink)
    ## inserer monnaie
    sendto(UDPServerSocket,bytes.fromhex("2404"))
    inserermonnaie =recerivefrom(UDPServerSocket)
    codeimonnaie=  checkIfMonnaieInserted(inserermonnaie)
    ## comparer
    compare(codedrink,codeimonnaie)
    ## recuperer monnaie
    #sendto(UDPServerSocket,bytes.fromhex("26"))
    #getmonnaie =recerivefrom(UDPServerSocket)
    #codeGetmonnaie=  checkGetMonnaie(getmonnaie)
    ## selectionner une boisson
    sendto(UDPServerSocket,first)
    bytesAddressPair =recerivefrom(UDPServerSocket)
    selectdrinknotpossible = checkIfCantSelectDrink(bytesAddressPair) 
