from operator import indexOf
import cv2
import numpy as np
import mediapipe as mp
import face_recognition
import os

#add images of team members in people folder. name of image should be name of the person
path = 'people'
imgs = []
names = []
people  = os.listdir(path)

def findEncodings(images):
    encodeList = []
    for img in images:
        encoding = face_recognition.face_encodings(img)[0]
        encodeList.append(encoding)
    return encodeList

for person in people:
    img = cv2.imread(f'{path}/{person}')
    imgs.append(img)
    names.append(os.path.splitext(person)[0])
    
encodeListKnown = findEncodings(imgs)

cap = cv2.VideoCapture(0)
while(True):
    _, frame = cap.read()
    facesInFrame = face_recognition.face_locations(frame)
    encodeFrame = face_recognition.face_encodings(frame)
    
    for encodeFace, faceLoc in zip(encodeFrame, facesInFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = names[matchIndex]
            y1, x2, y2, x1 = faceLoc
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xff == ord('x'):
        break
    
cap.release()
cv2.destroyAllWindows()