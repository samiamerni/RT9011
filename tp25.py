import socket
import time
import datetime
import json
import csv
import os
localIP     = "10.188.168.50"
localPort   = 3000
Portmachine   = 4200
bufferSize  = 1024
msgFromServer  = "120"


idTp = "TP/COM/PRT/BO-26"
reqid_1=1
null_ = "NaN"
v1_ = "v1"
time_data = 0


listelogname = ["Time","IdTp","reqID","Action","MessageType","lenghtString","Attendu","Observe","Verdic", "Message","VersionOutil"]
listeinit = []
listedata_1 = []
listedata_2 = []
listedata_3 = []
listedata_4 = []
listedata_5 = []
listedata_6 = []
listedata_7 = []
listedata_8 = []
listedata_9 = []

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
    UDPServerSocket.bind((localIP, localPort))
    return UDPServerSocket

def sendto(UDPServerSocket,bytesToSend):
    UDPServerSocket.sendto(bytesToSend, (localIP, 4200))
    return bytesToSend



def checkIfCanSelectDrink(bytesAddressPair,msgsend,idreq):
    if bytesAddressPair != "inconc":
        msgreturn_=bytesAddressPair[0]
        coderesult = bytesAddressPair[0][1:2] 
        resultreq=[time_data,idTp,idreq,msgsend,coderesult,null_]
        listedata_3.extend(resultreq)
        coderesult = int.from_bytes(coderesult, "big")    
        if coderesult == 1 :
            print('une boisson a été selectionnée')
            datasuccess="success"
            dataverdic="pass"
            resultsucess= [datasuccess,datasuccess,dataverdic,msgreturn_,v1_]
            listedata_3.extend(resultsucess)
            return coderesult
        else:
            print('aucune boisson n\'a été selectionnée')   
            dataverdic="error"
            resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
            listedata_3.extend(resulterror)
            return dataverdic
    else:
        print('il est impossible de Conclure')


def checkIfValidateDrink(bytesAddressPair,msgsend,idreq):
    if bytesAddressPair != "inconc":
        msgreturn_=bytesAddressPair[0]
        coderesult = bytesAddressPair[0][1:2]
        coderesult = int.from_bytes(coderesult, "big")
        resultreq=[time_data,idTp,idreq,msgsend,null_,null_]
        listedata_4.extend(resultreq)  
        if coderesult == 1 :
            print('une boisson est validée')
            datasuccess="success"
            dataverdic="pass"
            resultsucess= [datasuccess,datasuccess,dataverdic,msgreturn_,v1_]
            listedata_4.extend(resultsucess)
            return coderesult
        else:
            print("la boisson n'a pas ete validé") 
            dataverdic="error"
            resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
            listedata_4.extend(resulterror)
            return coderesult
    else:
        print('il est impossible de Conclure')

def checkIfMonnaieInserted(bytesAddressPair,msgsend,idreq):   
    if bytesAddressPair != "inconc":
        msgreturn_=bytesAddressPair[0]
        codemonnaie = bytesAddressPair[0][1:2] 
        resultreq=[time_data,idTp,idreq,msgsend,codemonnaie,null_]
        listedata_5.extend(resultreq)
        codemonnaie = int.from_bytes(codemonnaie, "big")    
        if codemonnaie == 1 :
            print("les pieces sont inserées")
            datasuccess="success"
            dataverdic="pass"
            resultsucess= [datasuccess,datasuccess,dataverdic,msgreturn_,v1_]
            listedata_5.extend(resultsucess)
            return codemonnaie
        else:
            print("les pieces ne sont pas inserées") 
            dataverdic="error"
            resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
            listedata_5.extend(resulterror)
            return codemonnaie
    else:
        print('il est impossible de Conclure')

def recupererboisson(bytesAddressPair,msgsend,idreq):
    if bytesAddressPair != "inconc":
        msgreturn_=bytesAddressPair[0]
        getdrink = bytesAddressPair[0][1:2] 
        resultreq=[time_data,idTp,idreq,msgsend,getdrink,null_]
        listedata_6.extend(resultreq)
        getdrink = int.from_bytes(getdrink, "big")    
        if getdrink == 0 :
            print("la boisson ne peut etre récupérer")
            dataverdic="error"
            resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
            listedata_6.extend(resulterror)
            
            return getdrink
        else:
            print("la boisson est récupérer")  
            datasuccess="success"
            dataverdic="pass"
            resultsucess= [datasuccess,datasuccess,dataverdic,msgreturn_,v1_]
            listedata_6.extend(resultsucess)
            return getdrink
    else:
        print('il est impossible de Conclure')

def recupererNbrGoblets(bytesAddressPair,msgsend,idreq,list):
    if bytesAddressPair != "inconc":
        msgreturn_=bytesAddressPair[0]
        coderesult =  bytesAddressPair[0][2:3]  
        resultreq=[time_data,idTp,idreq,msgsend,coderesult,null_]
        list.extend(resultreq)
        coderesult =int.from_bytes(coderesult, "big")
        print("le nbr de sucre est de: ",coderesult)
        datasuccess="success"
        dataverdic="pass"
        resultsucess= [datasuccess,datasuccess,dataverdic,msgreturn_,v1_]
        list.extend(resultsucess)
        return coderesult
    else:
        print('il est impossible de Conclure')
 

def checkIfMonnaieRecuperer(bytesAddressPair,msgsend,idreq):
    if bytesAddressPair != "inconc":
        msgreturn_=bytesAddressPair[0]
        codemonnaie = bytesAddressPair[0][1:2] 
        resultreq=[time_data,idTp,idreq,msgsend,codemonnaie,null_]
        listedata_7.extend(resultreq)
        codemonnaie = int.from_bytes(codemonnaie, "big")    
        if codemonnaie == 1 :    
            print("les pieces sont récupérées ") 
            datasuccess="success"
            dataverdic="pass"
            resultsucess= [datasuccess,datasuccess,dataverdic,msgreturn_,v1_]
            listedata_7.extend(resultsucess)
            return codemonnaie
        else:
            print("les pieces ne sont pas récupérés soit le prix de la boisson est égal aux pièces insérées, soit la boisson n'est pas entièrement payé")
            dataverdic="error"
            resulterror = [dataverdic,dataverdic,dataverdic,msgreturn_,v1_]
            listedata_7.extend(resulterror)
            return codemonnaie
    else:
        print('il est impossible de Conclure')

def compareGoblets(avant,apres):
    if avant > apres:
        print('nombre de goblets deminué')
        return True
    else:
        print('nombre de goblets n\'est pas deminué')
        return False

def logfile():
    with open("log.csv", 'a', encoding='UTF8', newline='') as flog:
        writer=csv.writer(flog)
        testfile=os.stat("log.csv").st_size == 0
        if testfile is True:
            writer.writerow(listelogname)
            if not listeinit:
                writer.writerow(listedata_1)
                writer.writerow(listedata_2)
                writer.writerow(listedata_3)
                writer.writerow(listedata_4)
                writer.writerow(listedata_5)
                writer.writerow(listedata_6)
                writer.writerow(listedata_7)
                writer.writerow(listedata_8)
            else:
                writer.writerow(listeinit)
                writer.writerow(listedata_1)
                writer.writerow(listedata_2)
                writer.writerow(listedata_3)
                writer.writerow(listedata_4)
                writer.writerow(listedata_5)
                writer.writerow(listedata_6)
                writer.writerow(listedata_7)
                writer.writerow(listedata_8)
        else:
                if not listeinit:
                    writer.writerow(listedata_1)
                    writer.writerow(listedata_2)
                    writer.writerow(listedata_3)
                    writer.writerow(listedata_4)
                    writer.writerow(listedata_5)
                    writer.writerow(listedata_6)
                    writer.writerow(listedata_7)
                    writer.writerow(listedata_8)
                else:
                    writer.writerow(listeinit)
                    writer.writerow(listedata_1)
                    writer.writerow(listedata_2)
                    writer.writerow(listedata_3)
                    writer.writerow(listedata_4)
                    writer.writerow(listedata_5)
                    writer.writerow(listedata_6)
                    writer.writerow(listedata_7)
                    writer.writerow(listedata_8)




## 02 latté | 01 italiano  | 03 cappucino | 04 good caffe | 05 Earl grey
## 06 green tea | 07 black tea | 08 soap | 00 americano


if __name__ == "__main__":
    idreq_1=2
    idreq_2=3
    idreq_3=4
    idreq_4=5
    idreq_5=6
    idreq_6=7
    idreq_7=8
    idreq_8=9
    first =  bytes.fromhex("2100")
    ## renitiliaser UT
    UDPServerSocket = initiateDatagram()
    initializeUT(UDPServerSocket)
    ## recuperer avant machine
    msgsend = sendto(UDPServerSocket,bytes.fromhex("10"))
    infos =recerivefrom(UDPServerSocket,msgsend,idreq_1)
    goblets_avant= recupererNbrGoblets(infos,msgsend,idreq_1,listedata_2)
    ## selectionner une boisson
    msgsend = sendto(UDPServerSocket,first)
    bytesAddressPair =recerivefrom(UDPServerSocket,msgsend,idreq_2)
    selectdrink = checkIfCanSelectDrink(bytesAddressPair,msgsend,idreq_2) 
    ### valider la boisson
    msgsend = sendto(UDPServerSocket,bytes.fromhex("23"))
    validatedrink =recerivefrom(UDPServerSocket,msgsend,idreq_3)
    codedrink = checkIfValidateDrink(validatedrink,msgsend,idreq_3)
    ## inserer monnaie
    msgsend = sendto(UDPServerSocket,bytes.fromhex("2404"))
    inserermonnaie =recerivefrom(UDPServerSocket,msgsend,idreq_4)
    codeimonnaie=  checkIfMonnaieInserted(inserermonnaie,msgsend,idreq_4)
    ### recuperer boisson
    msgsend = sendto(UDPServerSocket,bytes.fromhex("25"))
    gettexte =recerivefrom(UDPServerSocket,msgsend,idreq_5)
    recupererboisson(gettexte,msgsend,idreq_5) 
    ### texte recuperer votre monnaie
    msgsend = sendto(UDPServerSocket,bytes.fromhex("26"))
    gettexte =recerivefrom(UDPServerSocket,msgsend,idreq_6)
    checkIfMonnaieRecuperer(gettexte,msgsend,idreq_6)
    ## recuperer avant machine
    sendto(UDPServerSocket,bytes.fromhex("10"))
    msgsend = sendto(UDPServerSocket,bytes.fromhex("10"))
    infos =recerivefrom(UDPServerSocket,msgsend,idreq_7)
    goblets_apres= recupererNbrGoblets(infos,msgsend,idreq_1,listedata_7)
    ### comaprer nbr goblets
    compareGoblets(goblets_avant,goblets_apres)
    logfile()
