import pyautogui
import numpy as np
import cv2
from keyinput import pressKey, releaseKey
import random
from intersection_math import getIntersection
from movement_math import getMovementDecision
import math
from time import time,sleep
from windowcapture import getWindowScreenshot
# kanye head is 56x76
#origin = pyautogui.locateOnScreen("zone.png")
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
    return (center,min_val)#the second value is kinda like a confidence value. For kanye it should be above 4 million
def dist(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
def distsq(a,b):
    return (a[0]-b[0])**2+(a[1]-b[1])**2

do_input = True
prev_paddle_pos = (233,200)
prev_movement_decision = (False,False)
prev_intersection=(0,0)
minradius=39
waiting_on_movement=False
#this should be able to be dynamic instead of hard-coded in case it's a different browser. the static method returns none for some reason
winname = "Don't let Kanye into his zone: Kanye Zone - Google Chrome"#WindowCapture.get_kanye_window_name()
origin = findImageCenter(getWindowScreenshot(winname),cv2.imread("zone.png"))[0]

offsetX=-210
offsetY=-210
origin = (int(origin[0])+offsetX,int(origin[1])+offsetY)
print(origin)
while(True):
    #returns black screen, see this: https://stackoverflow.com/questions/59350839/capturing-screenshots-with-win32api-python-returns-black-image
    screenshot=getWindowScreenshot(winname)
    #cv2.imshow("raw screenshot",screenshot)
    #print(time())
    print(screenshot.shape)

    img = screenshot[origin[1]:origin[1]+466,origin[0]:origin[0]+465]
    cv2.imshow("raw img",img)
    #old way using pyautogui
    #screenshot = np.array(pyautogui.screenshot())

    #screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    #offsetX=-190
    #offsetY=-190
    #img = screenshot[origin.top+offsetY:origin.top+offsetY+466,origin.left+offsetX:origin.left+offsetX+465]#crops image to only the game screen

    radius=minradius

    for i in range(minradius,minradius+20):
        x=465//2+i
        (b,g,r) = img[466//2][x]
        if r>g+20 and b>g+20:#check if pixel is purple by seeing if the r and b are significantly greater than green
            radius=i
            minradius=i
        else:
            break
    img = cv2.circle(img,(465//2,466//2),radius,(0,0,255),2)


    (kanye_head_center,kanye_conf) = findImageCenter(img,kanyehead)
    if kanye_conf<4000000:#this is what the confidence is usually when it picks out the silhoutte instead of kanye himself
        continue
    topleft= (int(kanye_head_center[0]-56/2),int(kanye_head_center[1]-76/2))
    botright=(int(kanye_head_center[0]+56/2),int(kanye_head_center[1]+76/2))
    img = cv2.rectangle(img, topleft, botright, (255,0,0), 2) #draws blue rect around kanye head
    (paddleCenter,paddle_conf) = findImageCenter(img,paddleimg)
    #print(paddle_conf)
    #print(paddleCenter)
    img = cv2.circle(img,paddleCenter,20,(0,0,255),thickness=-1)#draw circle on paddle
    img = cv2.putText(img,f"{paddle_conf}",(50,50),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1,color=(255,255,255))
    if prevpos != None:
        delta = (kanye_head_center[0]-prevpos[0], kanye_head_center[1]-prevpos[1])
        intersection = getIntersection(center=kanye_head_center, delta=delta,radius=radius)
        #print(f"intersection: {intersection}")
        #intersection=(233+39,233)
        if(intersection!=None):
            #draw circle on intersection
            img = cv2.circle(img, (int(intersection[0]),int(intersection[1])), 10, color=(0, 255, 0), thickness=-1)


            if do_input:
                if dist(paddleCenter,prev_paddle_pos)<1.8*radius:
                    waiting_on_movement=False
                do_move_counter_clockwise,do_press_space = getMovementDecision(paddleCenter,intersection)
                #don't press space if:
                # - we pressed space but haven't seen the paddle move yet
                
                if do_press_space and not waiting_on_movement:#dist(intersection,prev_intersection)<radius*1.4):
                    waiting_on_movement=True
                    #print(f"current paddle: {paddleCenter}, previous paddle: {prev_paddle_pos}, prev_decision: {prev_movement_decision}, current intersection: {intersection}")
                    pressKey(0x39)#space
                    releaseKey(0x39)
                if do_move_counter_clockwise:
                    #cv2.circle(img,(100,100),100,(0,255,0),thickness=-1)
                    releaseKey(0x20)#D
                    pressKey(0x1E)#A
                else:
                    #cv2.circle(img,(100,100),100,(0,0,255),thickness=-1)
                    releaseKey(0x1E)#A
                    pressKey(0x20)#D
                prev_movement_decision=(do_move_counter_clockwise, do_press_space)
            prev_paddle_pos=paddleCenter
            prev_intersection=intersection
                
        #img = cv2.line(img, center, prevpos, color=(0, 0, 255), thickness=2) draws line in direction of travel
    prevpos = kanye_head_center
    cv2.imshow("img", img)#cv2.resize(img, (800, 450)))
    key = cv2.waitKey(1)
    if key == 27:#escape
        cv2.destroyAllWindows()
        break
    elif key == 112:#p key
        do_input = not do_input

print("exiting!")