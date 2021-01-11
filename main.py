import pyautogui
import numpy as np
import cv2
from keyinput import pressKey, releaseKey
import random
from intersection_math import getIntersection
from movement_math import getMovementDecision
import math
# kanye head is 56x76
rdown = False
ldown = False
origin = pyautogui.locateOnScreen("topleft.png", confidence=0.99)
print(origin)
#origin = Box{"left":origin.left+10,"top":origin.top+10}
prevpos = None


kanyehead = cv2.imread("kanye2.png")
paddleimg = cv2.imread("paddle.png")
            
def findImageCenter(background,img):    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
    h=img.shape[0]
    w=img.shape[1]
    res = cv2.matchTemplate(background, img, 0)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    #img = cv2.rectangle(img, top_left, bottom_right, 255, 2) draws blue rect around kanye head

    center = (top_left[0]+w//2, top_left[1]+h//2)
    return center


while(True):
    releaseKey(0x39)#so that it only gets held for one frame
    #releaseKey(0x1E)
    #releaseKey(0x20)
    img = pyautogui.screenshot()
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = img[origin.top+7:origin.top+466,origin.left+8:origin.left+465]
    img = cv2.circle(img,(465//2,466//2),39,(0,0,255),2)


    #img = cv2.rectangle(img, top_left, bottom_right, 255, 2) draws blue rect around kanye head
    center = findImageCenter(img,kanyehead)
    if prevpos != None:
        delta = (center[0]-prevpos[0], center[1]-prevpos[1])
        intersection = getIntersection(center=center, delta=delta)
        #print(f"intersection: {intersection}")
        #intersection=(233+39,233)
        if(intersection!=None):
            img = cv2.circle(img, (int(intersection[0]),int(intersection[1])), 10, color=(0, 255, 0), thickness=-1)#draw circle on intersection
            paddleCenter = findImageCenter(img,paddleimg)
            #print(paddleCenter)
            img = cv2.circle(img,paddleCenter,20,(0,0,255),thickness=-1)#draw circle on paddle
            #paddleCenterCorrected = (paddleCenter[0]-origin.left,paddleCenter[1]-origin.top)

            do_move_counter_clockwise,space = getMovementDecision(paddle_location=paddleCenter,target_location=intersection)
            if space:
                #print(f"paddle: {paddleCenter},target: {intersection}")
                pressKey(0x39)#space
            if do_move_counter_clockwise:
                #cv2.circle(img,(100,100),100,(0,255,0),thickness=-1)
                releaseKey(0x20)#D
                pressKey(0x1E)#A
            else:
                #cv2.circle(img,(100,100),100,(0,0,255),thickness=-1)
                releaseKey(0x1E)#A
                pressKey(0x20)#D
                
        #img = cv2.line(img, center, prevpos, color=(0, 0, 255), thickness=2) draws line in direction of travel
    prevpos = center
    cv2.imshow("img", img)#cv2.resize(img, (800, 450)))

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break
