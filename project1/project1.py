import cv2 as cv
import numpy as np

myColors = [
    [79, 90, 35, 255, 16, 255], #Green
    [90, 113, 231, 255, 107, 217] #Blue
]

myColorValues = [
    [70, 235, 52], #Green
    [52, 168, 235] #Blue
]

myPoints = [] #[x, y, colorId]


def empty(a):
    pass


def findColor(img, myColors):
    imgHsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv.inRange(imgHsv, lower, upper)
        cv.imshow(str(color[0]), mask)
        x, y = getContours(mask)
        cv.circle(imgResult, (x, y), 10, myColorValues[count], cv.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1

    return newPoints


def getContours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0

    for contour in contours:
        area = cv.contourArea(contour)
        if area > 500:
            cv.drawContours(imgResult, contour, -1, (255, 0, 0), 3)
            perimeter = cv.arcLength(contour, True)
            approximate = cv.approxPolyDP(contour, 0.02 * perimeter, True)
            x, y, w, h = cv.boundingRect(approximate)

    return x + w // 2, y


def drawOnCanvas(points, colorValues):
    for point in points:
        cv.circle(imgResult, (point[0], point[1]), 10, colorValues[point[2]], cv.FILLED)



frameWidth, frameHeight = 800, 600

cap = cv.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 130)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(imgResult, myColors)

    if len(newPoints) != 0:
        for newPoint in newPoints:
            myPoints.append(newPoints)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv.imshow("Result", imgResult)
    if cv.waitKey(1) & 0XFF == ord('q'):
        break

