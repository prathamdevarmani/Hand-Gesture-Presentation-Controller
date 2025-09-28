from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

# Parameters
width, height = 1280, 720
gestureThreshold = 300
folderPath = "Presentation"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
imgList = []
delay = 30
buttonPressed = False
counter = 0
imgNumber = 0
annotations = []
annotationNumber = -1
annotationStart = False
hs, ws = 120, 213  # height and width of small image (webcam overlay)

# Get list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

# Check if folder has images
if not pathImages:
    print("No images found in '{}' folder. Please add some images (e.g., slide1.jpg, slide2.jpg) and run again.".format(folderPath))
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Initial slide load
pathFullImage = os.path.join(folderPath, pathImages[imgNumber])

while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgCurrent = cv2.imread(pathFullImage)
    imgCurrent = cv2.resize(imgCurrent, (width, height))  # Resize slide to match screen dimensions

    # Find the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # with draw
    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:  # If hand is detected
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

        # Constrain values for easier drawing (map hand position to slide coordinates)
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  # If hand is at the height of the face (gesture zone)
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = []
                    annotationNumber = -1
                    annotationStart = False
                    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = []
                    annotationNumber = -1
                    annotationStart = False
                    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])

        # Drawing and pointer modes (only below gesture threshold to avoid interference)
        if cy > gestureThreshold:
            if fingers == [0, 1, 1, 0, 0]:  # Pointer mode (e.g., peace sign)
                cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

            if fingers == [0, 1, 0, 0, 0]:  # Index finger up for drawing
                if annotationStart is False:
                    annotationStart = True
                    annotations.append([])  # Start a new stroke
                    annotationNumber = len(annotations) - 1
                annotations[annotationNumber].append(indexFinger)
                cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            else:
                annotationStart = False  # Stop drawing when finger down

            if fingers == [0, 1, 1, 1, 0]:  # Three fingers for undo last stroke
                if annotations:
                    annotations.pop(-1)
                    if len(annotations) > 0:
                        annotationNumber = len(annotations) - 1
                    else:
                        annotationNumber = -1
                    annotationStart = False
                    buttonPressed = True

    else:
        annotationStart = False  # Stop drawing if no hand

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    # Draw all annotations (lines for each stroke)
    for annotation in annotations:
        for j in range(1, len(annotation)):
            if len(annotation) > 1:
                cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    # Overlay small webcam feed on bottom-right of slide
    imgSmall = cv2.resize(img, (ws, hs))
    imgCurrent[height - hs: height, width - ws: width] = imgSmall

    cv2.imshow("Slides", imgCurrent)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()