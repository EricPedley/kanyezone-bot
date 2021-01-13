import pyautogui
import numpy as np
import cv2
from keyinput import pressKey, releaseKey
import random
from intersection_math import getIntersection
from movement_math import getMovementDecision
import math
# kanye head is 56x76
origin = pyautogui.locateOnScreen("zone.png")

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
    #cv2.rectangle(img, top_left, bottom_right, (255,0,0), 2) #draws blue rect around kanye head

    center = (top_left[0]+w//2, top_left[1]+h//2)
    return center

do_input = False
while(True):
    #releaseKey(0x39)#so that it only gets held for one frame
    #releaseKey(0x1E)
    #releaseKey(0x20)
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    offsetX=-190
    offsetY=-190
    img = screenshot[origin.top+offsetY:origin.top+offsetY+466,origin.left+offsetX:origin.left+offsetX+465]#crops image to only the game screen

    radius=39
    for i in range(39,150):
        x=465//2+i
        (b,g,r) = img[466//2][x]
        if r>g+20 and b>g+20:#check if pixel is purple by seeing if the r and b are significantly greater than green
            radius=i
        else:
            break
    img = cv2.circle(img,(465//2,466//2),radius,(0,0,255),2)


    center = findImageCenter(img,kanyehead)
    topleft= (int(center[0]-56/2),int(center[1]-76/2))
    botright=(int(center[0]+56/2),int(center[1]+76/2))
    img = cv2.rectangle(img, topleft, botright, (255,0,0), 2) #draws blue rect around kanye head
    paddleCenter = findImageCenter(img,paddleimg)
    #print(paddleCenter)
    img = cv2.circle(img,paddleCenter,20,(0,0,255),thickness=-1)#draw circle on paddle
    if prevpos != None:
        delta = (center[0]-prevpos[0], center[1]-prevpos[1])
        intersection = getIntersection(center=center, delta=delta,radius=radius)
        #print(f"intersection: {intersection}")
        #intersection=(233+39,233)
        if(intersection!=None):
            img = cv2.circle(img, (int(intersection[0]),int(intersection[1])), 10, color=(0, 255, 0), thickness=-1)#draw circle on intersection
            
            #paddleCenterCorrected = (paddleCenter[0]-origin.left,paddleCenter[1]-origin.top)

            do_move_counter_clockwise,space = getMovementDecision(paddle_location=paddleCenter,target_location=intersection)
            if space:
                if do_input:
                    pressKey(0x39)#space
                    releaseKey(0x39)
                    
            if do_move_counter_clockwise:
                #cv2.circle(img,(100,100),100,(0,255,0),thickness=-1)
                if do_input:
                    releaseKey(0x20)#D
                    pressKey(0x1E)#A
            else:
                #cv2.circle(img,(100,100),100,(0,0,255),thickness=-1)
                if do_input:
                    releaseKey(0x1E)#A
                    pressKey(0x20)#D
                
        #img = cv2.line(img, center, prevpos, color=(0, 0, 255), thickness=2) draws line in direction of travel
    prevpos = center
    cv2.imshow("img", img)#cv2.resize(img, (800, 450)))
    key = cv2.waitKey(1)
    if key == 27:#escape
        cv2.destroyAllWindows()
        break
    elif key == 112:#p key
        do_input = not do_input
