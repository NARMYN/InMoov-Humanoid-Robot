import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
import time
from STT import speechrecognition
def decode_sentence(mysentence):
    my_data_arr =[0, 0, 0, 0, 0]
    mydict ={"thumb": 0, "index": 1, "middle": 2, "ring": 3, "pinky": 4}
    my_sentence_arr = mysentence.split()
    open_arr = [my_sentence_arr[i+1] for i in range(my_sentence_arr) if my_sentence_arr[i] == "open"]
    close_arr = [my_sentence_arr[i+1] for i in range(my_sentence_arr) if my_sentence_arr[i] == "close"]
    for finger in open_arr:
        if finger == "all":
            my_data_arr[1, 1, 1, 1, 1]
            break
        my_data_arr[mydict[finger]]=1
    for finger in close_arr:
        if finger == "all":
            my_data_arr[0, 0, 0, 0, 0]
            break
        my_data_arr[mydict[finger]]=0
    return my_data_arr
def write_data(data_arr, mySerial):
    mydata = str(data_arr[0])+str(data_arr[1])+str(data_arr[2])+str(data_arr[3])+str(data_arr[4])
    if mydata == "00000":
        mySerial.write(b'A')
    elif mydata == "00001":
        mySerial.write(b'B')
    elif mydata == "00010":
        mySerial.write(b'C')
    elif mydata == "00011":
        mySerial.write(b'D')
    elif mydata == "00100":
        mySerial.write(b'E')
    elif mydata == "00101":
        mySerial.write(b'F')
    elif mydata == "00110":
        mySerial.write(b'G')
    elif mydata == "00111":
        mySerial.write(b'H')
    elif mydata == "01000":
        mySerial.write(b'I')
    elif mydata == "01001":
        mySerial.write(b'J')
    elif mydata == "01010":
        mySerial.write(b'K')
    elif mydata == "01011":
        mySerial.write(b'L')
    elif mydata == "01100":
        mySerial.write(b'M')
    elif mydata == "01101":
        mySerial.write(b'N')
    elif mydata == "01110":
        mySerial.write(b'O')
    elif mydata == "01111":
        mySerial.write(b'P')
    elif mydata == "10000":
        mySerial.write(b'Q')
    elif mydata == "10001":
        mySerial.write(b'R')
    elif mydata == "10010":
        mySerial.write(b'S')
    elif mydata == "10011":
        mySerial.write(b'T')
    elif mydata == "10100":
        mySerial.write(b'U')
    elif mydata == "10101":
        mySerial.write(b'V')
    elif mydata == "10110":
        mySerial.write(b'W')
    elif mydata == "10111":
        mySerial.write(b'X')
    elif mydata == "11000":
        mySerial.write(b'Y')
    elif mydata == "11001":
        mySerial.write(b'Z')
    elif mydata == "11010":
        mySerial.write(b'1')
    elif mydata == "11011":
        mySerial.write(b'2')
    elif mydata == "11100":
        mySerial.write(b'3')
    elif mydata == "11101":
        mySerial.write(b'4')
    elif mydata == "11110":
        mySerial.write(b'5')
    elif mydata == "11111":
        mySerial.write(b'6')
def cvbased():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1, detectionCon=0.7)
    mySerial = serial.Serial(port = 'COM6', baudrate=9600)
    while cap.isOpened():
        success, img = cap.read()
        #detector.findHands(img)
        lmlist, bbox= detector.findHands(img)
        if lmlist:
            fingers=detector.fingersUp(lmlist[0])
            write_data(fingers, mySerial)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
def voicebased():
    mySerial = serial.Serial(port = 'COM5', baudrate=9600)
    while True:
        mybool=bool(input("Do you want to use speech recognition(Y/N)?"))
        if mybool==True:
            sentence = str(speechrecognition())
            sentence.lower()
            fingers = decode_sentence(sentence)
            print(fingers)
            write_data(fingers, mySerial)
        time.sleep(5)
voicebased()



'''import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, detectionCon=0.7)
#mySerial = serial.Serial(port = 'COM4', baudrate=9600)
while cap.isOpened():
    success, img = cap.read()
    #detector.findHands(img)
    lmlist, bbox= detector.findHands(img)
    if lmlist:
        fingers=detector.fingersUp(lmlist[0])
        print(fingers)
        #mySerial.write(fingers)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()'''
'''import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, detectionCon=0.7)
mySerial = serial.Serial(port = 'COM5', baudrate=9600)
while cap.isOpened():
    success, img = cap.read()
    #detector.findHands(img)
    lmlist, bbox= detector.findHands(img)
    if lmlist:
        fingers=detector.fingersUp(lmlist[0])
        mydata = str(fingers[0])+str(fingers[1])+str(fingers[2])+str(fingers[3])+str(fingers[4])
        print(mydata)
        if mydata == "10000":
            mySerial.write(b'H')
        else:
            mySerial.write(b'L')
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()'''

'''
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        fingers1 = detector.fingersUp(hand1)

        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmark points
            bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"

            fingers2 = detector.fingersUp(hand2)

            # Find Distance between two Landmarks. Could be same hand or different hands
            length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)  # with draw
            # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()'''

'''
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        fingers1 = detector.fingersUp(hand1)

        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmark points
            bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"

            fingers2 = detector.fingersUp(hand2)

            # Find Distance between two Landmarks. Could be same hand or different hands
            length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)  # with draw
            # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()'''       
'''from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        fingers1 = detector.fingersUp(hand1)

        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmark points
            bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"

            fingers2 = detector.fingersUp(hand2)

            # Find Distance between two Landmarks. Could be same hand or different hands
            length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)  # with draw
            # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()'''
