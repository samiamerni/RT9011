import socket
import datetime
import json
import time
import json
import csv
import os

localIP     = "localhost"
myIP     = "localhost"
localPort   = 3000
Portmachine   = 4200
bufferSize  = 1024
msgFromServer  = "120"


idTp = "TP/COM/PRT/BO-28"
reqid_1=1
null_ = "NaN"
v1_ = "v1"
time_data = 0


listelogname = ["Time","IdTp","reqID","Action","MessageType","lenghtString","Attendu","Observe","Verdic", "Message","VersionOutil"]
listeinit = []
listedata_1 = []
listedata_2 = []
listedata_3 = []



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

def recerivefrom(UDPServerSocket,msgsend,idreq):
    print("UDP server up and listening")
    listedata_1 = []
    # Listen for incoming datagrams
    global time_data
    time_data= datetime.datetime.fromtimestamp(time.time())
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        return bytesAddressPair
    except socket.timeout:
        initverdic="inconc"
        resultinc=[time_data,idTp,idreq,msgsend,null_,null_,null_,null_,initverdic,null_,v1_]
        listedata_1.extend(resultinc)
        return initverdic

def initiateDatagram():
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((myIP, localPort))
    return UDPServerSocket

def sendto(UDPServerSocket,bytesToSend):
    UDPServerSocket.sendto(bytesToSend, (localIP, 4200))
    return bytesToSend




def checkIfCanSelectDrink(bytesAddressPair,msgsend,idreq):
    if bytesAddressPair != "inconc":
        msgreturn_=bytesAddressPair[0]
        coderesult = bytesAddressPair[0][1:2] 
        resultreq=[time_data,idTp,idreq,msgsend,coderesult,null_]
        listedata_2.extend(resultreq)
        coderesult = int.from_bytes(coderesult, "big")    
        if coderesult == 1 :
            print('une boisson a été selectionnée')
            dataverdic="error"
            resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
            listedata_2.extend(resulterror)
            return dataverdic
        else:
            print('aucune boisson n\'a été selectionnée')   
            datasuccess="success"
            dataverdic="pass"
            resultsucess= [datasuccess,datasuccess,dataverdic,msgreturn_,v1_]
            listedata_2.extend(resultsucess)
            return coderesult
    else:
        print('il est impossible de Conclure')



def DrinkSetToZero(bytesAddressPair,msgsend,idreq):
    if bytesAddressPair != "inconc":
        msgreturn_=bytesAddressPair[0]
        coderesult = bytesAddressPair[0][1:2] 
        resultreq=[time_data,idTp,idreq,msgsend,coderesult,null_]
        listedata_1.extend(resultreq)
        coderesult =int.from_bytes(coderesult, "big")
        if coderesult == 1:
            print("la boisson n'est plus disponible ( mis a zero)")
            datasuccess="success"
            dataverdic="pass"
            resultsucess= [datasuccess,datasuccess,dataverdic,msgreturn_,v1_]
            listedata_1.extend(resultsucess)
            return coderesult
        else:
            print("echou de ma  mise a zero de la boisson")
            dataverdic="error"
            resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
            listedata_1.extend(resulterror)
            return dataverdic
    else:
        print('il est impossible de Conclure')


def logfile():
    with open("log.csv", 'a', encoding='UTF8', newline='') as flog:
        writer=csv.writer(flog)
        testfile=os.stat("log.csv").st_size == 0
        if testfile is True:
            writer.writerow(listelogname)
            if not listeinit:
                writer.writerow(listedata_1)
                writer.writerow(listedata_2)
            else:
                writer.writerow(listeinit)
                writer.writerow(listedata_1)
                writer.writerow(listedata_2)
        else:
                if not listeinit:
                    writer.writerow(listedata_1)
                    writer.writerow(listedata_2)
                else:
                    writer.writerow(listeinit)
                    writer.writerow(listedata_1)
                    writer.writerow(listedata_2)
## 02 latté | 01 italiano  | 03 cappucino | 04 good caffe | 05 Earl grey
## 06 green tea | 07 black tea | 08 soap | 00 americano


if __name__ == "__main__":
    idreq_1=2
    idreq_2=3
    first =  bytes.fromhex("2100")
    ## renitiliaser UT
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    ### set nb drinks to zero
    msgsend = sendto(UDPServerSocket,bytes.fromhex("040000"))
    bytesAddressPair =recerivefrom(UDPServerSocket,msgsend,idreq_1)
    DrinkSetToZero(bytesAddressPair,msgsend,idreq_1)
    ## selectionner une boisson
    msgsend = sendto(UDPServerSocket,first)
    bytesAddressPair =recerivefrom(UDPServerSocket,msgsend,idreq_1)
    selectdrink = checkIfCanSelectDrink(bytesAddressPair,msgsend,idreq_1) 
    logfile() 
