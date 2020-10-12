import cv2 as cv
import numpy as np

img = cv.imread("./Resources/dark-souls.jpg")

width, height = 151, 147

pts1 = np.float32([[374, 75], [393, 218], [499, 216], [519, 85]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv.getPerspectiveTransform(pts1, pts2)
imgOutput = cv.warpPerspective(img, matrix, (width, height))
cv.imshow("Image", imgOutput)
cv.waitKey(0)