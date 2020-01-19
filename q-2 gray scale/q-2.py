import cv2
import numpy as np
img = cv2.imread("test1.jpg")
red = img[:, :, 2].copy()
green = img[:, :, 1].copy()
blue = img[:, :, 0].copy()

Y = 0.21626*red + 0.7152*green + 0.0722*blue 
ans = Y.astype(np.uint8)

print(Y.shape)
print(img.shape)

cv2.imwrite("answer.bmp",ans)
cv2.imshow("result",ans)
cv2.waitKey(0)
cv2.destroyAllwindows()