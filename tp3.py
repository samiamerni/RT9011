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
idTp = "TP/COM/PRT/BO-03"
reqid_1=1
reqid_2=2
reqid_3=3
null_ = "NaN"
v1_ = "v1"
time_data = 0

listelogname = ["Time","IdTp","reqID","Action","MessageType","lenghtString","Attendu","Observe","Verdic", "Message","VersionOutil"]
listeinit = []
listedata_1 = []
listedata_2 = []


# Opening JSON file
def openconfigfile():
    f = open('../config.json')
    data = json.load(f)
    stringjson = data["strings"]
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

def sendto(UDPServerSocket,bytesToSend):
    UDPServerSocket.sendto(bytesToSend, (localIP, 4200))
    return bytesToSend

def recerivefrom(UDPServerSocket,msgsend):
    print("UDP server up and listening")
    # Listen for incoming datagrams
    global time_data
    time_data= datetime.datetime.fromtimestamp(time.time())
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        return bytesAddressPair
    except socket.timeout:
        initverdic="inconc"
        resultinc=[time_data,idTp,reqid_2,msgsend,null_,null_,null_,null_,initverdic,null_,v1_]
        listedata_1.extend(resultinc)
        return initverdic

def decodeprice(bytesAddressPair,stringjson,msgsend):
    if bytesAddressPair != "inconc":
        messageType = bytesAddressPair[0][:1]
        lent = bytesAddressPair[0][1:2]
        split3 = bytesAddressPair[0][2:]
        msgreturn_=bytesAddressPair[0]
        stringresult = split3.decode("utf-8")
        lent = int.from_bytes(lent, "big") 
        resultreq=[time_data,idTp,reqid_3,msgsend,messageType,lent]
        listedata_2.extend(resultreq)
        messageType = int.from_bytes(messageType, "big")  ### equivalent de x11 est 17 en entier
        if stringjson["changeText"] == stringresult or stringjson["chooseDrinkText"] == stringresult or stringjson["drinkMadeText"] == stringresult or stringjson["noBucket"] == stringresult :
            print('le prix n\'est pas affiché')
            dataverdic="error"
            resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
            listedata_2.extend(resulterror)
            return dataverdic
        else:
            print('le prix de la boisson est :',stringresult)
            datasucess="success"
            dataverdic="pass"
            resultsuccess= [stringresult,datasucess,dataverdic,msgreturn_,v1_]
            listedata_2.extend(resultsuccess)
            return datasucess
    else:
        print('il est impossible de Conclure')

def decodeDrinkSelected(bytesAddressPair,msgsend):
    if bytesAddressPair != "inconc":
        msgreturn_=bytesAddressPair[0]
        coderesult = bytesAddressPair[0][1:2] 
        resultreq=[time_data,idTp,reqid_2,msgsend,coderesult,null_]
        listedata_1.extend(resultreq)
        coderesult = int.from_bytes(coderesult, "big")    
        if coderesult == 1 :
            print('une boisson a été selectionnée')
            datasuccess="success"
            dataverdic="pass"
            resultsucess= [datasuccess,datasuccess,dataverdic,msgreturn_,v1_]
            listedata_1.extend(resultsucess)
            return datasuccess
        else:
            print('aucune boisson n\'a été selectionnée')   
            dataverdic="error"
            resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
            listedata_1.extend(resulterror)
            return dataverdic
    else:
        print('il est impossible de Conclure')


## 02 latté | 01 italiano  | 03 cappucino | 04 good caffe | 05 Earl grey
## 06 green tea | 07 black tea | 08 soap | 00 americano

def logfile():
    with open("log.csv", 'a', encoding='UTF8', newline='') as flog:
        writer=csv.writer(flog)
        testfile=os.stat("log.csv").st_size == 0
        if testfile is True:
            writer.writerow(listelogname)
            writer.writerow(listeinit)
            writer.writerow(listedata_1)
            writer.writerow(listedata_2)
        else:
            writer.writerow(listeinit)
            writer.writerow(listedata_1)
            writer.writerow(listedata_2)


if __name__ == "__main__":
    bytesToSend =  bytes.fromhex("2100")
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    ## check if a drink is selected
    #sendto(UDPServerSocket,bytesToSend)
    msgsend = sendto(UDPServerSocket,bytesToSend)
    bytesAddressPair =recerivefrom(UDPServerSocket,msgsend)
    drinkSelected =decodeDrinkSelected(bytesAddressPair,msgsend)
    ### check if price is printed
    #sendto(UDPServerSocket,bytes.fromhex("12"))
    msgsend = sendto(UDPServerSocket,bytes.fromhex("12"))
    validatedrink =recerivefrom(UDPServerSocket,msgsend)
    stringjson = openconfigfile()
    decodeprice(validatedrink,stringjson,msgsend)
    logfile()
    



 












