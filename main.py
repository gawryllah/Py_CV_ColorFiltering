import cv2
import numpy as np
import os
import sys



colors = []

if len(str(sys.argv[1:])) > 2:

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, str(sys.argv[1:]))
else:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "res/rgb_ball_720.mp4")

cap = cv2.VideoCapture(filename)

fps = int(cap.get(cv2.CAP_PROP_FPS))
hueValue = 0
satuValue = 0
vValue = 0


def setColors(b, g, r):

    if len(colors) == 0:
        colors.append(b)
        colors.append(g)
        colors.append(r)
    else:
        colors[0] = b
        colors[1] = g
        colors[2] = r
    pass

def chSatu(frame, value):
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h = hsv_img[:, :, 0]
    s = hsv_img[:, :, 1]
    v = hsv_img[:, :, 2]
    hsv_new = None
    bgr_new = None

    if(value < 255 and value > 1):
        
        snew = np.mod(s + value, 180).astype(np.uint8)

        hsv_new = cv2.merge([h,snew,v])
        bgr_new = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
        print(f"satu change value: {value}")


    

    return bgr_new
    pass

def changeValue(frame, value):
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h = hsv_img[:, :, 0]
    s = hsv_img[:, :, 1]
    v = hsv_img[:, :, 2]
    hsv_new = None
    bgr_new = None

    if(value < 255 and value > 1):
        
        vnew = np.mod(v + value, 180).astype(np.uint8)

        hsv_new = cv2.merge([h,s,vnew])
        bgr_new = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
        print(f"value change value: {value}")



    return bgr_new
    pass

def changeHue(frame, value):
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h = hsv_img[:, :, 0]
    s = hsv_img[:, :, 1]
    v = hsv_img[:, :, 2]
    hsv_new = None
    bgr_new = None


    if(value < 179 and value > 1):
        
        hnew = np.mod(h + value, 180).astype(np.uint8)

        hsv_new = cv2.merge([hnew,s,v])
        bgr_new = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
        print(f"hue change value: {value}")

    


    return bgr_new
    pass

def maskImg(col, frame):
    lowerColors = np.array([col[0]-10, col[1]-10, col[2]-10])
    upperColors = np.array([col[0]+10, col[1]+10, col[2]+10])

    x = cv2.inRange(frame, lowerColors, upperColors)
    z = cv2.bitwise_and(frame, frame, mask=x)

    z = cv2.cvtColor(z, cv2.COLOR_HSV2BGR)

    return z
    pass

def getColorMask(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colorsB = frame[y,x,0]
        colorsG = frame[y,x,1]
        colorsR = frame[y,x,2]

        setColors(colorsB, colorsG, colorsR)
    pass


cv2.namedWindow('Video')
cv2.setMouseCallback('Video',getColorMask)

if (cap.isOpened()== False):

  print("Error opening video stream or file")


while(cap.isOpened()):

  ret, frame = cap.read()

  if ret == True:

  
    
    key = cv2.waitKey(fps)
    if key == ord('q'):
        break
        
    elif key == ord('p'):
        key = cv2.waitKey(-1)
        if key == ord('q'):
            break
        cv2.imshow("Video",frame)
    elif key == ord('a'):
        hueValue += 10
        frame = changeHue(frame, hueValue)
        cv2.imshow("Video",frame)
    elif key == ord('z'):
        hueValue -= 10
        frame = changeHue(frame, hueValue)
        cv2.imshow("Video",frame)
    elif key == ord('e') and len(colors) != 0:
        frame = maskImg(colors,frame)
        cv2.imshow("Video",frame)
    elif key == ord('s'):
        satuValue += 10
        frame = chSatu(frame, satuValue)
        cv2.imshow("Video",frame)
    elif key == ord('x'):
        satuValue -= 10
        frame = chSatu(frame, satuValue)
        cv2.imshow("Video",frame)
    elif key == ord('d'):
        vValue += 10
        frame = changeValue(frame, vValue)
        cv2.imshow("Video",frame)
    elif key == ord('c'):
        vValue -= 10
        frame = changeValue(frame, vValue)
        cv2.imshow("Video",frame)
    else:
        cv2.imshow("Video",frame)
  else:
    break
 
cap.release()

cv2.destroyAllWindows()