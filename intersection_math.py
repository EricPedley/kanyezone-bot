import math

# returns the x and y coords of the intersection with a circle
def getLineCircleIntersection(delta, center):
    if delta[0]==0:
        delta=(1e-10,delta[1])
    a = delta[1]/delta[0]  # slope of line
    b = center[1]-a*center[0]  # y intercept of line
    c = 465//2  # canvas width/2
    d = 466//2  # canvas height/2
    e = 39  # circle radius
    negb = -2*(a*(b-d)-c)
    bsq = negb**2
    neg4ac = -4*(a*a+1)*(b**2-2*b*d+d**2+c**2-e**2)
    if bsq + neg4ac > 0:  # two solutions
        x1=(negb+math.sqrt(bsq+neg4ac))/(2*(a**2+1))
        x2=(negb-math.sqrt(bsq+neg4ac))/(2*(a**2+1))
        return ((x1,x1*a+b),(x2,x2*a+b))
    elif bsq + neg4ac == 0:  # one solutions
        x = negb/(2*(a**2+1))
        return ((x,x*a+b))#x*a+b
    else:  # no intersection
        return None

# kanye head is 56x76

def getIntersection(delta, center):
    d=delta
    c=center
    for i in range(5):  # maximum iterations is 5 before it gives up trying to find an intersect
        intersections = getLineCircleIntersection(d, c)
        # the following conditions checks whether there are intersections and whether one of them is
        if intersections != None:
            if (intersections[0][0] > c[0]) == (d[0] > 0) or (intersections[1][0] > c[0]) == (d[0] > 0):
                return intersections
        else:  # there are no intersections and we need to find the equation for the reflected line
            
            if d[0]==0:
                d=(1e-10,d[1])
            slope = d[1]/d[0]
            yint = 233  # the y coordinate at whichever side edge of the map, except this starts at halfway because it needs to be assigned here but idk to what, and 233 is between both
            if d[0] >= 0:  # kanye is moving to the right
                # the y coordinate at the right edge of the map, with the right edge coordinate hard coded in
                yint = slope*(465-c[0])+c[1]
            else:  # kanye is moving to the left
                yint = slope*-c[0]+c[1]
            if yint > 466:  # intersection with top, which in the coordinate system is zero
                d = (d[0], -d[1])
                c = (c[0]-c[1]/slope, 0)
            elif yint < 0:
                d = (d[0], -d[1])
                c = (c[0]+(466-c[1])/slope, 0)
            else:  # bouncing off a side wall
                d = (-d[0], d[1])
                c = (0 if d[0] < 0 else 465, yint)
    return None