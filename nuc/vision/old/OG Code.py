import cv2
import PIL
import numpy as np
import time
import math

def switchGR(img):
    (B, G, R) = cv2.split(img)
    return cv2.merge([B, R, G])

def colorMask(color):
    """
    #0 = red
    #1 = green
    """
    return np.logical_and.reduce((img[:,:,0]<65, img[:,:,1+color] < 50, img[:,:,2-color]>60))

def firstIndex(list,x):
    for i in range(len(list)):
        if list[i] == x:
            return i
    raise ValueError("{} is not in list".format(x))

def lastIndex(list,x):
    for i in reversed(range(len(list))):
        if list[i] == x:
            return i
    raise ValueError("{} is not in list".format(x))

###Drawing rectange###
img = cv2.imread("./testVision/justDoImage.png",1)
img = cv2.resize(img, (0,0),fx=0.2,fy=0.2)

#Change here#
color = 0

if color:
    img = switchGR(img)

mask = colorMask(color)

y,x = np.where(mask)
img = cv2.rectangle(img, (np.min(x), np.min(y)), (np.max(x), np.max(y)), (0,255,255), 3)
###

# ### Alternatives to finding indexes of a value in array to consdier
# # print(np.nonzero(y == max(y)))
# # print(np.where(y == max(y)))

# # Coordinate of left pixel
# xLeft,yLeft = np.min(x),y[lastIndex(x,min(x))] # Maybe use variable for min(x) earlier

# # Coordinate of right pixel
# xRight,yRight = np.max(x),y[lastIndex(x,max(x))]

# # Coordinate of top pixel
# xTop, yTop = x[int((firstIndex(y,np.min(y))+lastIndex(y,np.min(y)))/2)],np.min(y)

# img[yLeft,xLeft] = (0,255,0)
# img[yRight,xRight] = (0,255,0)
# img[yTop,xTop] = (0,255,0)

# cv2.line(img,(xLeft,yLeft),(xTop,yTop),(255,0,0),2)
# cv2.line(img,(xRight,yRight),(xTop,yTop),(255,0,0),2)

# angLeft = math.atan2(yLeft-yTop, xTop-xLeft)/2/math.pi*360
# angRight = math.atan2(yRight-yTop, xRight-xTop)/2/math.pi*360
# angDiff = 90-angLeft-angRight

# print(angLeft)
# print(angRight)
# print(30/angDiff)

###Drawing edges###


edges = cv2.Canny(img,100,200)

###

# cv2.imshow("image",img)
cv2.imshow("edges",edges)
cv2.waitKey()