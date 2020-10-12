import cv2 as cv
import numpy as np

widthImg, heightImg = 480, 720

cap = cv.VideoCapture(0)
cap.set(3, heightImg)
cap.set(4, widthImg)
cap.set(10, 150)


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


def preProcessing(img):
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv.Canny(imgBlur, 200, 200)
    kernel = np.ones((5, 5))
    imgDilation = cv.dilate(imgCanny, kernel, iterations=2)
    imgThreshold = cv.erode(imgDilation, kernel, iterations=1)

    return imgThreshold


def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 5000:
            #cv.drawContours(imgContour, contour, -1, (255, 0, 0), 3)
            perimeter = cv.arcLength(contour, True)
            approximate = cv.approxPolyDP(contour, 0.02 * perimeter, True)
            if area > maxArea and len(approximate) == 4:
                biggest = approximate
                maxArea = area
    cv.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest


def reorder(points):
    points = points.reshape((4, 2))
    newPoints = np.zeros((4, 1, 2), np.int32)
    add = points.sum(1)

    newPoints[0] = points[np.argmin(add)]
    newPoints[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    newPoints[1] = points[np.argmin(diff)]
    newPoints[2] = points[np.argmax(diff)]
    return newPoints


def getWarp(img, biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv.warpPerspective(img, matrix, (widthImg, heightImg))
    imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    imgCropped = cv.resize(imgCropped, (widthImg, heightImg))
    return imgCropped


while True:
    success, img = cap.read()
    cv.resize(img, (widthImg, heightImg))
    imgContour = img.copy()

    imgThreshold = preProcessing(img)
    biggest = getContours(imgThreshold)

    if biggest.size != 0:
        imgWarpped = getWarp(img, biggest)
        imgArray = ([img, imgThreshold, imgContour, imgWarpped])
    else:
        imgArray = ([img, imgThreshold, imgContour, img])

    stack = stackImages(0.6, imgArray)
    cv.imshow("Stack", stack)
    cv.imshow("Warped", imgArray[len(imgArray) - 1])

    if cv.waitKey(1) & 0XFF == ord('q'):
        break

