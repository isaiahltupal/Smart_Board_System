import cv2
import numpy as np

img = cv2.imread("../resources/image/image.jpg")

print(img)

cv2.imshow("Image",img)
cv2.waitKey(0)


