import cv2 as cv
import numpy as np

img = cv.imread("./Resources/dark-souls.jpg")
imgResize = cv.resize(img, (1080, 720))
imgCropped = imgResize[0:500, 50:500]

cv.imshow("Normal", img)
cv.imshow("Resized", imgResize)
cv.imshow("Cropped", imgCropped)
cv.waitKey(0)