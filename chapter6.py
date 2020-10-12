import cv2 as cv
import numpy as np

img = cv.imread("./Resources/dark-souls.jpg")

imgHor = np.vstack((img, img))

cv.imshow("Horizontal", imgHor)
cv.waitKey(0)