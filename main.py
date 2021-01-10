import pyautogui
import numpy as np
import cv2
from keyinput import pressKey, releaseKey
import random
from intersection_math import getIntersection
# kanye head is 56x76
rdown = False
ldown = False
origin = pyautogui.locateOnScreen("topleft.png", confidence=0.99)
print(origin)
prevpos = None



            


while(True):
    img = pyautogui.screenshot()
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    template = cv2.imread("kanye2.png")
    h = template.shape[0]
    w = template.shape[1]
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
    res = cv2.matchTemplate(img, template, 0)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    #img = cv2.rectangle(img, top_left, bottom_right, 255, 2) draws blue rect around kanye head

    center = (top_left[0]+w//2, top_left[1]+h//2)
    if prevpos != None:
        delta = (center[0]-prevpos[0], center[1]-prevpos[1])
        intersection = getIntersection(center=(center[0]-origin.left, center[1]-origin.top), delta=delta)
        print(f"intersection: {intersection}")
        if intersection!=None:
            img = cv2.circle(img, (origin.left+int(intersection[0][0]),origin.top+int(intersection[0][1])), 10, color=(0, 255, 0), thickness=-1)
            

        #print(delta)
        #img = cv2.line(img, center, prevpos, color=(0, 0, 255), thickness=2) draws line in direction of travel
    prevpos = center
    cv2.imshow("img", cv2.resize(img, (800, 450)))
   # print(cv2.matchTemplate(img,cv2.imread("kanye2.png"),0))
    # cv2.rectangle(img,(origin.left,origin.top),(origin.left+origin.width,origin.top+origin.height),color=(0,255,0),thickness=2)
    # if(origin):
    #     img = drawRect(img, origin, (0, 255, 0), 2)
    # res = pyautogui.locateOnScreen('kanye2.png', confidence=0.8)
    # if(res):
    #     img = drawRect(img,res,(255,0,0),2)
    # cv2.imshow("img", cv2.resize(img, (800, 450)))
    # if(random.random()>0.5):
    #     pressKey(0x1E)#A
    #     releaseKey(0x20)
    # else:
    #     pressKey(0x20)#D
    #     releaseKey(0x1E)

    # cv2.imshow("screenshot",img)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break
