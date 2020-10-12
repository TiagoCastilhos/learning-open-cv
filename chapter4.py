import cv2 as cv
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)
#img[:] = 255, 0, 0
#cv.rectangle(img, (0, 0), (255, 350), (0, 255, 255), cv.FILLED)
cv.circle(img, (400, 50), 30, (255, 255, 0), cv.FILLED)
cv.putText(img, "   OPEN CV    ", (300, 100), cv.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 1)

cv.imshow("Image", img)
cv.waitKey(0)