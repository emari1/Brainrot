# Source - https://stackoverflow.com/a
# Posted by Ahmet
# Retrieved 2025-11-20, License - CC BY-SA 4.0

import cv2
import mediapipe  as mp
from cvzone.HandTrackingModule import HandDetector

img3 = cv2.imread('.venv/iu_.png')
img4 = cv2.imread(".venv/somethng.png")

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=.8, maxHands=2)

mp_drawing=mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

roi_x1, roi_y1 = 0, 0
roi_w, roi_h = 300, 300


while cap.isOpened():
    success, img = cap.read()
    roi_x1 = (frameWidth - roi_w) // 2
    roi_y1 = (frameHeight - roi_h) // 2
    roi_x2 = roi_x1 + roi_w
    roi_y2 = roi_y1 + roi_h
    cv2.rectangle(img, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)
    if success:
        RGB_frame=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hands, img = detector.findHands(img)

        if hands:
            hand1=hands[0]
            fingers1=detector.fingersUp(hand1)

            lmList1=hand1["lmList"]
            bbox1=hand1["bbox"] # x y width height
            centerPoint1=hand1["center"]
            handType1=hand1["type"]
            ##print(fingers1)
            if fingers1[1]==1 and sum(fingers1) == 1:
                print("bazinga")
                x = 0
                x=x+1
                cv2.imshow("Bazinga", img3)
            else:
                cv2.destroyWindow("Bazinga")



            ##print(handType1)
            if(len(hands)==2):
                hand2=hands[1]
                lmList2=hand2["lmList"]
                handType2 = hand2["type"]
                fingers2 = detector.fingersUp(hand2)
                print(fingers1,fingers2)
                cx1, cy1 = hand1["center"]
                cx2, cy2 = hand2["center"]
                hand1_in_box = (roi_x1 <= cx1 <= roi_x2) and (roi_y1 <= cy1 <= roi_y2)
                hand2_in_box = (roi_x1 <= cx2 <= roi_x2) and (roi_y1 <= cy2 <= roi_y2)

                if hand1_in_box and hand2_in_box and sum(fingers1)==5 and sum(fingers2)==5:
                    print("Both hands are inside the box!")
                    cv2.imshow("HUH", img4)
                else:
                    cv2.destroyWindow("HUH")


        cv2.imshow("Result", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
