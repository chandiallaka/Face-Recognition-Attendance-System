import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import pyttsx3

path = 'Attendence'  # Setting Path of Images
Images = []  # To load all athe images form the folder to Images array
ImageNames = []  # This array is to print the names in OP
MyList = os.listdir('Attendence')  # Grabing the Images we can put path also inplace of attendence
encodeList_saved = []
# print(MyList)

# Loading & Reading Images
for cls in MyList:  # MyList has the list of all images in it & that will be there in cls also
    curImg = face_recognition.load_image_file(f'{path}/{cls}')  # Readed image will be stored in curImg
    # printing MyList & cls gives same o/p Images gives the readed file
    Images.append(curImg)
    ImageNames.append(os.path.splitext(cls)[0])  # Adding images names into ImagesNames array w/o extensinon
    # print(cls)
# print(path)
print(ImageNames)

print(type(ImageNames))


# Encoding of Images
def findEncodings(Images):
    for img in Images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList_saved.append(encode)
        print(encode)
    return encodeList_saved


def markAttendence(name):
    with open('Attendence.csv', 'a+') as f:
        myDataList = f.readlines()
        nameList = []
        # print(myDataList)
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


encodeListKnown = findEncodings(Images)
print(len(encodeListKnown))
size = len(encodeListKnown)
# print(encodeList_saved)
print('Encoding Complete')

cap = cv2.VideoCapture(0)  # Initializing web cap

i = 1
value = "nomatch"
markedlist = ["hello"]

marked = False
while True:
    sucess, img = cap.read()  # dought about sucess
    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # reducing the size of image
    imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # finding the rgb

    faceCurFrame = face_recognition.face_locations(imgs)  # finding locations because webcam may include many faces
    encodeCurFrame = face_recognition.face_encodings(imgs,faceCurFrame)  # finding encodings of all images in the web ca
    # matches = face_recognition.compare_faces(encodeListKnown,encodeCurFrame)
    # cv2.rectangle(img, faceCurFrame([3], faceCurFrame[0]), (faceCurFrame[1], faceCurFrame[2]), (255, 0, 255), 2)  # adjusting borders

    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):  # finding the matches of all images captured in the web cam with our saved encodings
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        '''print(faceDis.item(-1))
        print(faceDis.item(-2))
        print(faceDis.item(-3))
        print(faceDis.item(0))
        print(faceDis.item(1))
        print(faceDis.item(2))'''

        # score

        # end score
        matchIndex = np.argmin(faceDis)
        name = ImageNames[matchIndex].upper()
        if matches[matchIndex]:
            lenth = len(markedlist)
            #print(lenth)
            # print(name)

            if (value != name):
                value = name
                i = 1

            if (value == name):
                i = i + 1

            #if(faceDis.item(0)<=0.4):

        if (i % 3) == 0:
            for x in range(lenth):
                if (name == markedlist[x]):
                    break
                for i in range(size-1):
                    if (x == (lenth - 1) and faceDis.item(i)<=0.4):
                        y1, x2, y2, x1 = faceLoc
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        print(name)
                        markAttendence(name)
                        engine = pyttsx3.init()
                        engine.say(name + "your attendence is marked")
                        markedlist.append(name)
                        engine.runAndWait()
    cv2.imshow('WebCam', img)

    k = cv2.waitKey(1)
    if (marked == True):
        break

    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

cap.release()
cv2.destroyAllWindows()