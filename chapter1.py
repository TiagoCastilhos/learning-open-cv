import cv2 as cv
print("package imported")

img = cv.imread("./Resources/dark-souls.jpg")

cv.imshow("Test", img)

cv.waitKey(0)