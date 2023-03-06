import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from csv import writer

###To Use screen capture
# from PIL import ImageGrab
# from PIL import Image

import msg
import imageBot
import sheet
import recieve
 
path = 'Images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

for cl in myList:
    if cl.endswith('.DS_Store'):
        continue
    else:    
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        dNames = [i[1:] for i in classNames]
        dType = [int(i[0:1]) for i in classNames]    
        # dNames.append('Unknown')    
        # dType.append(3)

print(dNames)
print(dType)
 
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
def markPresence(name):
    with open('log.csv','a') as f:
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        entry=[f'{name}',f'{dType[dNames.index(name)]}',f'{dtString}']

        writer_object=writer(f)
        writer_object.writerow(entry)

        f.close()

def uLog(name):
    with open('log.csv','a') as f:
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        entry=[f'{name}',3,f'{dtString}']

        writer_object=writer(f)
        writer_object.writerow(entry)

        f.close()


def notify1(mName):
    if(ctr>0):
        msg.send(1, mName)
        imageBot.main('FAMILY_CHAT_ID')

def notify2(mName, imgCap):
    if(ctr>0):
        msg.send(2, mName, imgCap)
        imageBot.main('LEA_CHAT_ID')
        imageBot.main('FAMILY_CHAT_ID')
        imageBot.main('VOLUNTEER_CHAT_ID')

def notify3():
    if(ctr>0):
        msg.send(3)
        imageBot.main('FAMILY_CHAT_ID')
        imageBot.main('VOLUNTEER_CHAT_ID')
        
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')
 
cap = cv2.VideoCapture(1)

ctr=0

while True:
    mType=3
    mName='Unknown'
    success, img = cap.read()
    # cv2.imwrite('Visitor.png',img)
    # imgPass='Visitor.png'
    # img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    check=False

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)
    
        if matches[matchIndex]:
            mName = dNames[matchIndex]
            mType = dType[matchIndex]
            check=True
            # print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4

            if(mType == 1):
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,mName,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                cv2.imwrite('Visitor.png',img)
                imgPass='Visitor.png'
                markPresence(mName)
                notify1(mName)
                ctr+=1
                
            elif(mType == 2):
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                cv2.putText(img,mName,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                cv2.imwrite('Visitor.png',img)
                imgPass='Visitor.png'
                markPresence(mName)
                notify2(mName, imgPass)
                ctr+=1

        elif(check==False):
            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,255),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,255),cv2.FILLED)
                mName='Unknown'
                cv2.putText(img,mName,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                cv2.imwrite('Visitor.png',img)
                imgPass='Visitor.png'
                notify3()
                ctr+=1

                if(ctr>1):
                    response=recieve.getText(FAMILY_CHAT_ID)
                    if(response=='Y'):
                        mname='Unknown Suspect'
                        uLog(mName)
                        notify2(mName, imgPass)
                        ctr+=1
                    elif(response=='N'):
                        ctr+=1
                        break
                    else:
                        ctr+=1
        sheet.writeSheet()
        
    cv2.imshow('WeSecure Image Recognition',img)
    cv2.waitKey(1)