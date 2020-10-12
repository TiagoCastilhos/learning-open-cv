import math

import cv2 as cv
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 500:
            cv.drawContours(imgContour, contour, -1, (255, 0, 0), 3)
            perimeter = cv.arcLength(contour, True)
            approximate = cv.approxPolyDP(contour, 0.02 * perimeter, True)
            objectCorners = len(approximate)
            x, y, w, h = cv.boundingRect(approximate)
            if objectCorners == 3:
                objectType = "Triangle"
            elif objectCorners == 4:
                if (w / float(h)) == 1:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objectCorners == 5:
                objectType = "Pentagon"
            elif objectCorners == 6:
                objectType = "Hexagon"
            elif objectCorners == 8: #Problem to differ circles from hearts
                rad = math.sqrt(area / math.pi)
                calcPerimeter = rad * 2 * math.pi
                difference = perimeter - calcPerimeter
                if difference > -20 and difference < 20:
                    objectType = "Circle"
                else:
                    objectType = "Heart"
            elif objectCorners == 10:
                objectType = "Star"
            else:
                objectType = "None"

            cv.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(imgContour, objectType,
                       (x + (w//2)-10, y + (h//2) - 10), cv.FONT_HERSHEY_COMPLEX,
                       0.6, (0, 0, 0), 2)


img = cv.imread("./Resources/shapes.png")
imgContour = img.copy()

grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blurImg = cv.GaussianBlur(grayImg, (7, 7), 1)
cannyImg = cv.Canny(blurImg, 50, 50)
getContours(cannyImg)

imgBlank = np.zeros_like(img)
imgStack = stackImages(0.8, ([img, grayImg, blurImg],
                             [cannyImg, imgContour, imgBlank]))

cv.imshow("Stack", imgStack)
cv.waitKey(0)