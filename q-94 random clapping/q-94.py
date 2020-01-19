import cv2
import numpy as np

def iou(img,img_part,k,u):
    def tem_matching(img,img_part):
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
        
        return Y,X
        
    H,W,C = img.shape
    Hp,Wp,Cp = img_part.shape
    #以下のx1 y1はくりぬく領域の左上の座標
    #random.seed(0)で発生する乱数をあらかじめ固定
    #random.randit(下限,上限,出力する件数)
    
    #0 padding
    out = np.zeros((H+2, W+2, C), dtype = np.float) #float
    out[1:H+1, 1:W+1] = img.copy().astype(np.float) #float
    Y, X = tem_matching(out,img_part)
    a = np.array((X,Y,X+Wp-1,Y+Hp-1), dtype = np.float32)

    np.random.seed(0)
    for j in range(k):
        print(j)
        x1 = np.random.randint(W-Wp)
        y1 = np.random.randint(H-Hp)
    
        #部分画像左上の座標

        b_point = [x1,y1]
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
        
        if iou >=u:
            l = (0,255,0)
        else:
            l = (255,0,0)
        
        out[b[1]-1:b[3]+1,b[0]-1] = l
        out[b[1]-1:b[3]+1,b[2]+1] = l
        out[b[1]-1,b[0]-1:b[2]+1] = l
        out[b[3]+1,b[0]-1:b[2]+1] = l

    #部分画像の場所を赤く囲む
    a = a.astype(np.uint8)
    m = (0,0,255)
    out[a[1]-1:a[3]+1,a[0]-1] = m
    out[a[1]-1:a[3]+1,a[2]+1] = m
    out[a[1]-1,a[0]-1:a[2]+1] = m
    out[a[3]+1,a[0]-1:a[2]+1] = m

    img = out[1:H+1,1:W+1]
    img = img.astype(np.uint8)
    return img
        


img = cv2.imread("penguin.bmp")
img_part = cv2.imread("penguin_face.bmp")

#kはクラッピング数
#uはiouの閾値。u以上の重なりの場合緑で表示
k = 200
u = 0.2


#paar画像と同じサイズでクリップ
img = iou(img,img_part,k,u)

cv2.imwrite("answer.bmp", img)
cv2.imshow("result", img)
cv2.waitKey(0)
cv2.destroyAllwindows()     
