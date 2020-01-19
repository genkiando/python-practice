
import cv2
import numpy as np

img = cv2.imread("test1.jpg")
result = img.copy()
result = result // 64 * 64 + 32


cv2.imwrite("answer.bmp", result)
cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllwindows()