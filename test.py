from screenshotexample import getWindowScreenshot
img = getWindowScreenshot("Don't let Kanye into his zone: Kanye Zone - Google Chrome")
print(img)
import cv2
cv2.imshow("bruh",img)
cv2.waitKey(0)
#WindowCapture.get_full_screenshot()










# intersection=(233,233-39)
#             delta
#             img = cv2.circle(img, (origin.left+int(intersection[0]),origin.top+int(intersection[1])), 10, color=(0, 255, 0), thickness=-1)
#             target_angle = math.atan((delta[1]-466)/(delta[0]-465))

#             paddleCenterCorrected = (paddleCenter[0]-origin.left,paddleCenter[1]-origin.top)
#             current_angle = math.atan((paddleCenterCorrected[1]-466//2)/(paddleCenterCorrected[0]-465//2))


#             if(paddleCenterCorrected[0]<465//2):
#                 current_angle+=math.pi

#             #we need the diff between paddleCenterCorrected and intersection
#             #dot product will be positive if they're in the same direction, 0 if perpendicular, and negative if in opposite directions
#             dotprod = dot(paddleCenterCorrected,intersection)
            
#             target_angle = (target_angle + 2*math.pi)%(2*math.pi)
#             ccw_ref_point = (50*math.cos(target_angle+math.pi/2),50*math.sin(target_angle+math.pi/2))#this point is 90 degrees counter clockwise of target angle. If the current angle is in the same direction, we need to press D to go clockwise, else we need to press A
#             dot2 = dot(ccw_ref_point,paddleCenterCorrected)
#             if dotprod>=0:# if in same direction, move toward target vector
#                 if dot2>0:
#                     print("pressing D")
#                     releaseKey(0x1E)#A
#                     pressKey(0x20)#D
#                 else:
#                     print("pressing A")
#                     pressKey(0x1E)#A
#                     releaseKey(0x20)#D
#             else:#if not in same direction, press spacebar and move in opposite direction
#                 pressKey(0x39)
#                 if dot2<=0:
#                     print("pressing D and space")
#                     releaseKey(0x1E)#A
#                     pressKey(0x20)#D
#                 else:
#                     print("pressing A and space")
#                     releaseKey(0x20)#D
#                     pressKey(0x1E)#A