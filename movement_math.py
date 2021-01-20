import math
import cv2
def dot(a,b):
    return (a[0]*b[0]+a[1]*b[1])
def get_rotated_vector(v,theta):#uses rotation matrix
    return (math.cos(theta)*v[0]-math.sin(theta)*v[1],math.sin(theta)*v[0]+math.cos(theta)*v[1])
class Box():
    def __init__(self,l,t):
        self.left=l
        self.top=t
# both parameters are tuples of xy coordinates relative to the origin, like in range [0,466]. the img parameter is for debugging by drawing on the image
# returns a tuple of booleans. The first is whether or not we try to spin counter clockwise, and the second is whether or not we press spacebar
def getMovementDecision(paddle_location,target_location, origin=None, img=None):
    canvas_center = (465//2,466//2)
        # the relative coordinates treat the canvas center like the origin
    relative_paddle = (paddle_location[0]-canvas_center[0],paddle_location[1]-canvas_center[1])
    relative_target =(target_location[0]-canvas_center[0],target_location[1]-canvas_center[1])
        # dot product will be positive if they're in the same direction, 0 if perpendicular, and negative if in opposite directions
    dotprod = dot(relative_paddle,relative_target)
        # this point is 90 degrees counter clockwise of target angle. If the current angle is in the same direction, we need to press D to go clockwise, else we need to press A
    
    #TODO use rotation matrix instead of converting to and from angles
    ccw_ref_point = get_rotated_vector(relative_target,math.pi/2)#(50*math.cos(target_angle+math.pi/2)+465//2, 50*math.sin(target_angle+math.pi/2)+466//2)
    #print(ccw_ref_point,relative_paddle)
    dot2 = dot(ccw_ref_point, relative_paddle)
    if dotprod>0:
        if dot2>0:
            return True,False
        else:
            return False,False
    else:#press space then move
        #print(paddle_location,target_location)
        if dot2>0:
            return False,True
        else:
            return True,True
#ccw,space = getMovementDecision(paddle_location=(465//2-39,466/2),target_location=(280,466/2-30))

print(getMovementDecision((226,248),(272,233)))
#print(getMovementDecision((115,238),(177,282))) 