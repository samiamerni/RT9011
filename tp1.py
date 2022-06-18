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
msgFromServer  = "12"
bytesToSend =  bytes.fromhex(msgFromServer)
idTp = "TP/COM/INFO/PRT/BO-01"
reqid_1=1
reqid_2=2
null_ = "NaN"
v1_ = "v1"
time_data = 0


listelogname = ["Time","IdTp","reqID","Action","MessageType","lenghtString","Attendu","Observe","Verdic", "Message","VersionOutil"]
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
        resultinc=[time_,idTp,reqid_1,msginitialiaze,null_,null_,null_,null_,initverdic,null_,v1_]
        listeinit.extend(resultinc)
        return initverdic
    
    coderp = returnUT[0][1:2]
    messageType = returnUT[0][:1]
    initmsgreturn_=returnUT[0]
    resultreq=[time_,idTp,reqid_1,msginitialiaze,messageType,null_,coderp]
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
        initfail="error"
        initverdic="error"
        resulterror = [initfail,initverdic,initmsgreturn_,v1_]
        listeinit.extend(resulterror)
        return initfail


def initiateDatagram():
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((myIP, localPort))
    return UDPServerSocket

def sendto_(UDPServerSocket):
    UDPServerSocket.sendto(bytesToSend, (localIP, 4200))

def recerivefrom(UDPServerSocket):
    print("UDP server up and listening")
    global time_data
    time_data= datetime.datetime.fromtimestamp(time.time())
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        return bytesAddressPair
    except socket.timeout:
        initverdic="inconc"
        resultinc=[time_data,idTp,reqid_2,bytesToSend,null_,null_,null_,null_,initverdic,null_,v1_]
        listedata.extend(resultinc)
        return initverdic

def decode(bytesAddressPair,stringjson):
    #rint(datetime.datetime.fromtimestamp(time.time()),bytesAddressPair[0])
    if bytesAddressPair != "inconc":
        messageType = bytesAddressPair[0][:1]
        lent = bytesAddressPair[0][1:2]
        split3 = bytesAddressPair[0][2:]
        msgreturn_=bytesAddressPair[0]
        stringresult = split3.decode("utf-8") 
        lent = int.from_bytes(lent, "big")  
        resultreq=[time_data,idTp,reqid_2,bytesToSend,messageType,lent]
        listedata.extend(resultreq)   
        messageType = int.from_bytes(messageType, "big")  ### equivalent de x11 est 17 en entier
        if stringresult.__eq__(stringjson) and messageType == 17 :
            print('aucune boisson n\'a été selectionnée et aucun prix n\'est affiché')
            datasucess="success"
            dataverdic="pass"
            resultsuccess= [stringresult,datasucess,dataverdic,msgreturn_,v1_]
            listedata.extend(resultsuccess)
            return datasucess
        else:
            print('une boisson est peut etre selectionné')   
            dataverdic="error"
            resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
            listedata.extend(resulterror)
            return dataverdic
    else:
        print('il est impossible de Conclure') 

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
    resultUT= initializeUT(UDPServerSocket)
    print("initialisateur:",resultUT)
    print(bytesToSend )
    sendto_(UDPServerSocket)
    bytesAddressPair =recerivefrom(UDPServerSocket)
    stringjson = openconfigfile()
    resultFinal= decode(bytesAddressPair,stringjson)
    print("resultat final",resultFinal)
    logfile()


 












