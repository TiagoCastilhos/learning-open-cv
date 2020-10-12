import cv2 as cv
import numpy as np

img = cv.imread("./Resources/dark-souls.jpg")
kernel = np.ones((5, 5), np.uint8)

imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
imgBlur = cv.GaussianBlur(imgGray, (5, 5), 0)
imgCanny = cv.Canny(img, 100, 100)
imgDialation = cv.dilate(imgCanny, kernel, iterations=1)
imgEroded = cv.erode(imgDialation, kernel, iterations=1)

cv.imshow("Gray", imgGray)
cv.imshow("Blur", imgBlur)
cv.imshow("Canny", imgCanny)
cv.imshow("Dialated", imgDialation)
cv.imshow("Eroded", imgEroded)

cv.waitKey(0)