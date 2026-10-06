import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, detectionCon=0.7)
mySerial = serial.Serial(port = 'COM6', baudrate=9600)
while cap.isOpened():
    success, img = cap.read()
    #detector.findHands(img)
    lmlist, bbox= detector.findHands(img)
    if lmlist:
        fingers=detector.fingersUp(lmlist[0])
        data = str(fingers[0])+str(fingers[1])+str(fingers[2])+str(fingers[3])+str(fingers[4])
        print(data)
        if data == "00000":
            mySerial.write(b'A')
        elif data == "00001":
            mySerial.write(b'B')
        elif data == "00010":
                mySerial.write(b'C')
        elif data == "00011":
                mySerial.write(b'D')
        elif data == "00100":
                mySerial.write(b'E')
        elif data == "00101":
                mySerial.write(b'F')
        elif data == "00110":
                mySerial.write(b'G')
        elif data == "00111":
                mySerial.write(b'H')
        elif data == "01000":
                mySerial.write(b'I')
        elif data == "01001":
                mySerial.write(b'J')
        elif data == "01010":
                mySerial.write(b'K')
        elif data == "01011":
                mySerial.write(b'L')
        elif data == "01100":
                mySerial.write(b'M')
        elif data == "01101":
                mySerial.write(b'N')
        elif data == "01110":
                mySerial.write(b'O')
        elif data == "01111":
                mySerial.write(b'P')
        elif data == "10000":
            mySerial.write(b'Q')
        elif data == "10001":
            mySerial.write(b'R')
        elif data == "10010":
            mySerial.write(b'S')
        elif data == "10011":
                mySerial.write(b'T')
        elif data == "10100":
                mySerial.write(b'U')
        elif data == "10101":
                mySerial.write(b'V')
        elif data == "10110":
                mySerial.write(b'W')
        elif data == "10111":
                mySerial.write(b'X')
        elif data == "11000":
                mySerial.write(b'Y')
        elif data == "11001":
                mySerial.write(b'Z')
        elif data == "11010":
                mySerial.write(b'1')
        elif data == "11011":
                mySerial.write(b'2')
        elif data == "11100":
                mySerial.write(b'3')
        elif data == "11101":
                mySerial.write(b'4')
        elif data == "11110":
                mySerial.write(b'5')
        elif data == "11111":
                mySerial.write(b'6')
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

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
