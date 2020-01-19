import cv2
img = cv2.imread("test1.jpg")
red = img[:, :, 2].copy()
green = img[:, :, 1].copy()
blue = img[:, :, 0].copy()

img[:, :, 1] = red
img[:, :, 2] = blue
img[:, :, 0] = green

cv2.imwrite("answer.bmp",img)
cv2.imshow("result",img)
cv2.waitKey(0)
cv2.destroyAllwindows()