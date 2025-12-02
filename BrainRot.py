import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector

## image paths
img3 = cv2.imread('./iu_.png')
img4 = cv2.imread("./somethng.png")
img5 = cv2.imread("./stoopidmeme.png")

## resolution
frameWidth = 1024
frameHeight = 768
cap = cv2.VideoCapture(1)

# Initialize the cvzone HandDetector
detector = HandDetector(detectionCon=.8, maxHands=2)

# Initialize MediaPipe utility objects
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Configure camera parameters
cap.set(3, frameWidth)  # width
cap.set(4, frameHeight)  # height
cap.set(10, 150)  # brightness


# scaling
def scale_image(image, width, height):
    if image is None:
        return None
    return cv2.resize(image, (width, height))


img3 = scale_image(img3, frameWidth, frameHeight)
img4 = scale_image(img4, frameWidth, frameHeight)
img5 = scale_image(img5, frameWidth, frameHeight)

# Green ROI dimensions (centered)
roi_w, roi_h = 300, 300

# Black ROI dimensions (centered)
roi2_w, roi2_h = 1000, 200

# Shift amount to the right (in pixels)
SHIFT_RIGHT = 150

while cap.isOpened():
    success, img = cap.read()

    if success:
        # Calculate ROI positions to center them on screen, then shift right
        roi_x1 = (frameWidth - roi_w) // 2 + SHIFT_RIGHT
        roi_y1 = (frameHeight - roi_h) // 2
        roi_x2 = roi_x1 + roi_w
        roi_y2 = roi_y1 + roi_h

        # Black ROI centered horizontally, below green ROI, also shifted right
        roi2_x1 = (frameWidth - roi2_w) // 2 + SHIFT_RIGHT
        roi2_y1 = roi_y2 + ((frameHeight - roi_y2 - roi2_h) // 2)
        roi2_x2 = roi2_x1 + roi2_w
        roi2_y2 = roi2_y1 + roi2_h

        # Draw black bounding box
        cv2.rectangle(img, (roi2_x1, roi2_y1), (roi2_x2, roi2_y2), (0, 0, 0), 2)

        # Draw green bounding box
        cv2.rectangle(img, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)

        # Convert BGR to RGB for MediaPipe
        RGB_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Detect hands
        hands, img = detector.findHands(img)

        if hands:
            hand1 = hands[0]
            fingers1 = detector.fingersUp(hand1)
            lmList1 = hand1["lmList"]
            centerPoint1 = hand1["center"]
            handType1 = hand1["type"]

            # If ONLY the index finger is up
            if fingers1[1] == 1 and sum(fingers1) == 1:
                print("bazinga")
                cv2.imshow("Bazinga", img3)
            else:
                cv2.destroyWindow("Bazinga")

            # If two hands detected
            if len(hands) == 2:
                hand2 = hands[1]
                lmList2 = hand2["lmList"]
                handType2 = hand2["type"]
                fingers2 = detector.fingersUp(hand2)

                # Get fingertip landmark positions
                tip_ids = [4, 8, 12, 16, 20]
                tips1 = [lmList1[i] for i in tip_ids]
                tips2 = [lmList2[i] for i in tip_ids]

                print(fingers1, fingers2)

                # Get center points
                cx1, cy1 = hand1["center"]
                cx2, cy2 = hand2["center"]


                # Count fingers in ROI1
                def count_fingers_in_roi(tips, x1, y1, x2, y2):
                    return sum(1 for (x, y, _) in tips if x1 <= x <= x2 and y1 <= y <= y2)


                MIN_FINGERS = 2

                count1 = count_fingers_in_roi(tips1, roi_x1, roi_y1, roi_x2, roi_y2)
                count2 = count_fingers_in_roi(tips2, roi_x1, roi_y1, roi_x2, roi_y2)

                fingers_in_box_1 = count1 >= MIN_FINGERS
                fingers_in_box_2 = count2 >= MIN_FINGERS

                # Check if hand1 is in ROI2
                hand1_in_roi2 = (roi2_x1 <= cx1 <= roi2_x2) and (roi2_y1 <= cy1 <= roi2_y2)
                hand2_in_roi2 = (roi2_x1 <= cx2 <= roi2_x2) and (roi2_y1 <= cy2 <= roi2_y2)

                if hand1_in_roi2 or hand2_in_roi2:
                    print("Hand is inside ROI2!")
                    cv2.imshow("6 7", img5)
                else:
                    cv2.destroyWindow("6 7")

                # If both hands' fingers are in the green ROI
                if fingers_in_box_1 and fingers_in_box_2:
                    print("Both hands' fingers are inside the ROI!")
                    cv2.imshow("HUH", img4)
                else:
                    cv2.destroyWindow("HUH")

        # Show main camera output
        cv2.imshow("Result", img)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()