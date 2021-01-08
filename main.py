import pyautogui
import numpy as np
import cv2
from keyinput import pressKey, releaseKey
import random
import math
# kanye head is 56x76
rdown = False
ldown = False
origin = pyautogui.locateOnScreen("topleft.png", confidence=0.99)
print(origin)
prevpos = None


# returns the x coords of the intersection with a circle
def getLineCircleIntersection(delta, center):
    a = delta[1]/delta[0]  # slope of line
    b = center[1]-a*center[0]  # y intercept of line
    c = 465//2  # canvas width/2
    d = 466//2  # canvas height/2
    e = 39  # circle radius
    negb = -2*(a*(b-d)-c)
    bsq = negb**2
    neg4ac = -4*(a*a+1)*(b**2-2*b*d+d**2+c**2-e**2)
    if bsq > neg4ac:  # two solutions
        return ((negb+math.sqrt(bsq+neg4ac))/(2*(a**2+1)), (negb-math.sqrt(bsq+neg4ac))/(2*(a**2+1)))
    elif bsq == neg4ac:  # one solutions
        return negb/(2*(a**2+1))
    else:  # no intersection
        return None


def getIntersection(delta, center):
    for i in range(10):  # maximum iterations is 10 before it gives up trying to find an intersect
        intersections = getLineCircleIntersection(delta, center)
        # the following conditions checks whether there are intersections and whether one of them is
        if intersections != None and (intersections[0][0] > center[0]) == (delta[0] > 0) or (intersections[1][0] > center[0]) == (delta[0] > 0):
            return intersections
        else:  # there are no intersections and we need to find the equation for the reflected line
            slope = delta[1]/delta[0]
            yint = 233  # the y coordinate at whichever side edge of the map, except this starts at halfway because it needs to be assigned here but idk to what, and 233 is between both
            if delta[0] >= 0:  # kanye is moving to the right
                # the y coordinate at the right edge of the map, with the right edge coordinate hard coded in
                yint = slope*(465-center[0])+center[1]
            else:  # kanye is moving to the left
                yint = slope*-center[0]+center[1]
            if yint > 466:  # intersection with top, which in the coordinate system is zero
                delta = (delta[0], -delta[1])
                center = (center[0]-center[1]/slope, 0)
            elif yint < 0:
                delta = (delta[0], -delta[1])
                center = (center[0]+(466-center[1])/slope, 0)
            else:  # bouncing off a side wall
                delta = (-delta[0], delta[1])
                center = (0 if delta[0] < 0 else 465, yint)


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
    img = cv2.rectangle(img, top_left, bottom_right, 255, 2)

    center = (top_left[0]+w//2, top_left[1]+h//2)
    if type(prevpos) != type(None):
        delta = (center[0]-prevpos[0], center[1]-prevpos[1])
        solution = None
        while(solution == None):
            intersection = getIntersection(
                (center[0]-origin.left, center[1]-origin.top), delta)
        print(delta)
        img = cv2.line(img, center, prevpos, color=(0, 0, 255), thickness=2)
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
