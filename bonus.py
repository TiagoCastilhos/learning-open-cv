#Viola & Jones
#Take faces, non faces, train and generate a xml file

import cv2 as cv
import numpy as np

faceCascade = cv.CascadeClassifier("./Resources/haarcascade_frontalface_default.xml")
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    imgGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(imgGray, 1.1, 6)

    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 125, 0), 2)

    cv.imshow("Stack", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()