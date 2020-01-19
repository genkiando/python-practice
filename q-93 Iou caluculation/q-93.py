import cv2
import numpy as np

img = cv2.imread("penguin.bmp")
img_part = cv2.imread("penguin_face.bmp")

H,W,C = img.shape
Hp,Wp,Cp = img_part.shape

# aはpenguinの顔部分　左からx1 y1（矩形左上） x2 y2（矩形右下） 
#　ｂは適当に選んだ領域
#　2つのＩｏｕ（重なり具合)を計算する
#　ＩｏU = |RoI| / |R1 + R2 -RoI|

#適当に選ぶ領域の左上の座標(x,y)
b_point = [10,200]
a = np.array((50,14,50+Wp-1,14+Hp-1), dtype = np.float32)
b = np.array((b_point[0],b_point[1],b_point[0]+Wp-1,b_point[1]+Hp-1), dtype = np.float32)

area_a = (a[2]-a[0])*(a[3]-a[1])
area_b = (b[2]-b[0])*(b[3]-b[1])

# x1 = a[0]
# y1 = a[1]
# x2 = a[2]
# y2 = a[3]

# X1 = b[0]
# Y1 = b[1]
# X2 = b[2]
# Y2 = b[3]

# 顔部分を基準に、矩形右上で重なる場合
# <= で同じ値のとき（重なったとき）に対応
# 
if a[0]<=b[0]<=a[2] and a[1]<=b[3]<=a[3]:
    roi = (a[2]-b[0])*(b[3]-a[1])
    iou = roi/(area_a + area_b -roi)
# 顔部分を基準に、矩形左下で重なる場合
# <= で同様に対応。これですべての重なり方を網羅

elif a[0]<b[2]<=a[2] and a[1]<b[1]<=a[3]:
    roi = (b[2]-a[0])*(a[3]-b[1])
    iou = roi/(area_a + area_b -roi)

# 顔部分を基準に、矩形左上で重なる場合
elif a[0]<b[2]<a[2] and a[1]<b[3]<a[3]:
    roi = (b[2]-a[0])*(b[3]-a[1])
    iou = roi/(area_a + area_b -roi) 

# 顔部分を基準に、矩形右下で重なる場合
elif a[0]<b[0]<[2] and a[1]<b[1]<a[3]:
    roi = (a[2]-b[0])*(a[3]-b[1])
    iou = roi/(area_a + area_b -roi) 
    
else:
    iou = 0

#ついでにどことどこを重ねたか表示
a = a.astype(np.int)
b = b.astype(np.int)

img[a[1]-1:a[3]+1,a[0]-1] = (0,0,255)
img[a[1]-1:a[3]+1,a[2]+1] = (0,0,255)
img[a[1]-1,a[0]-1:a[2]+1] = (0,0,255)
img[a[3]+1,a[0]-1:a[2]+1] = (0,0,255)
    
img[b[1]-1:b[3]+1,b[0]-1] = (0,255,0)
img[b[1]-1:b[3]+1,b[2]+1] = (0,255,0)
img[b[1]-1,b[0]-1:b[2]+1] = (0,255,0)
img[b[3]+1,b[0]-1:b[2]+1] = (0,255,0)

print(iou)

cv2.imwrite("answer.bmp", img)
cv2.imshow("result", img)
cv2.waitKey(0)
cv2.destroyAllwindows()        