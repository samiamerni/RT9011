import socket
import time
import datetime
import json
import csv
import os

localIP     = "192.168.56.9"
myIP     = "192.168.56.1"
localPort   = 3000
Portmachine   = 4200
bufferSize  = 1024
idTp = 2
null_ = "NaN"
msgFromServer  = "23"
bytesToSend =  bytes.fromhex(msgFromServer)
v1_ = "v1"
time_data = 0


listelogname = ["Time","IdTp","Action","RepId","lenghtString","Attendu","Observe","Verdic", "Message","VersionOutil"]
listeinit = []
listedata = []

# Opening JSON file
def openconfigfile():
    f = open('../config.json')
    data = json.load(f)
    stringjson = data["strings"]["chooseDrinkText"]
    return stringjson

def initializeUT(UDPServerSocket):
    print("initialisation de UT")
    successut = 1  ### x01 en entier est 1   1 == succes 0 == echoue
    msginitialiaze=bytes.fromhex("00") # idtest initialiaze = 0
    UDPServerSocket.sendto(msginitialiaze, (localIP, 4200))
    time_= datetime.datetime.fromtimestamp(time.time())
    try:
        returnUT = UDPServerSocket.recvfrom(bufferSize)
    except socket.timeout:
        initverdic="inconc"
        resultinc=[time_,idTp,msginitialiaze,null_,null_,null_,null_,initverdic,null_,v1_]
        listeinit.extend(resultinc)
        return initverdic
    
    coderp = returnUT[0][1:2]
    repid = returnUT[0][:1]
    initmsgreturn_=returnUT[0]
    resultreq=[time_,idTp,msginitialiaze,repid,null_,coderp]
    listeinit.extend(resultreq)
    if successut.__eq__(int.from_bytes(coderp, "big")) :
        print("initialisation UT reussite")
        initsucess="success"
        initverdic="pass"
        resultsuccess= [initsucess,initverdic,initmsgreturn_,v1_]
        listeinit.extend(resultsuccess)
        return initsucess
    else:
        print("initialisation UT echoué")
        initfail="erreur"
        initverdic="fail"
        resulterror = [initfail,initverdic,initmsgreturn_,v1_]
        listeinit.extend(resulterror)
        return initfail


def initiateDatagram():
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((myIP, localPort))
    return UDPServerSocket

def sendto(UDPServerSocket):
    UDPServerSocket.sendto(bytesToSend, (localIP, 4200))

def recerivefrom(UDPServerSocket):
    print("UDP server up and listening")
    # Listen for incoming datagrams
    global time_data
    time_data= datetime.datetime.fromtimestamp(time.time())
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    except socket.timeout:
        initverdic="inconc"
        resultinc=[time_data,idTp,bytesToSend,null_,null_,null_,null_,initverdic,null_,v1_]
        listedata.extend(resultinc)
        return initverdic
    return bytesAddressPair

def decodevalidate(bytesAddressPair):
    msgreturn_=bytesAddressPair[0]
    coderesult = bytesAddressPair[0][1:2]
    coderesult = int.from_bytes(coderesult, "big")
    print(bytesToSend) 
    resultreq=[time_data,idTp,bytesToSend,null_,null_]
    listedata.extend(resultreq)  
    if coderesult == 0 :
        print('on ne peut pas validé la boisson tant qu\'on ne l\'a pas selectionné')
        datasuccess="success"
        dataverdic="pass"
        resultsucess= [datasuccess,datasuccess,dataverdic,msgreturn_,v1_]
        listedata.extend(resultsucess)
        return datasuccess
    else:
        print('une boisson est validée')  
        dataverdic="error"
        resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
        listedata.extend(resulterror)
        return dataverdic


def logfile():
    with open("log.csv", 'a', encoding='UTF8', newline='') as flog:
        writer=csv.writer(flog)
        testfile=os.stat("log.csv").st_size == 0
        if testfile is True:
            writer.writerow(listelogname)
            writer.writerow(listeinit)
            writer.writerow(listedata)
        else:
            writer.writerow(listeinit)
            writer.writerow(listedata)


if __name__ == "__main__":
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    ### check if we can validate drink
    sendto(UDPServerSocket)
    validatedrink =recerivefrom(UDPServerSocket)
    decodevalidate(validatedrink)
    logfile()
    



 












