import cv2 as cv
import numpy as np

minArea = 500
color = (255, 0, 255)
widthImg, heightImg = 480, 640
cap = cv.VideoCapture(0)
cap.set(3, widthImg)
cap.set(4, heightImg)
cap.set(10, 150)
count = 0
nPlateCascade = cv.CascadeClassifier("../Resources/haarcascade_russian_plate_number.xml")

while True:
    success, img = cap.read()
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv.putText(img, "NumberPlate", (x, y - 5), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            imgRoi = img[y:y+h, x:x+w]
            cv.imshow("ROI", img)

    cv.imshow("Result", img)

    if cv.waitKey(1) & 0XFF == ord('s'):
        cv.imwrite("../Resources/Scanned/NoPlate_" + str(count) + ".jpg", imgRoi)
        cv.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv.FILLED)
        cv.putText(img, "Scan saved", (150, 265), cv.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
        cv.imshow("Result", img)
        cv.waitKey(500)
        count += 1

    if cv.waitKey(1) & 0XFF == ord('q'):
        break
