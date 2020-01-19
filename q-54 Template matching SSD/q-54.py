import cv2
import numpy as np

img = cv2.imread("penguin.bmp")
img_part = cv2.imread("penguin_face.bmp")

H,W,C = img.shape
Hp,Wp,Cp = img_part.shape

k=1000000
Y=-1
X=-1

for y in range(H-Hp):
    for x in range(W-Wp):
        s= np.sum((img[y:y+Hp,x:x+Wp]-img_part)**2).astype(np.float)
        if s < k:
            k=s
            Y=y
            X=x

print([X,Y,Hp-1,Wp-1])

img[Y-1:Y+Hp+2,X-1] = (0,0,255)
img[Y-1:Y+Hp+2,X+Wp+1] = (0,0,255)
img[Y-1,X-1:X+Wp+1] = (0,0,255)
img[Y+Hp+1,X-1:X+Wp+1] = (0,0,255)

#cv2.imwrite("answer.bmp", img)
#cv2.imshow("result", img)
#cv2.waitKey(0)
#cv2.destroyAllwindows()

