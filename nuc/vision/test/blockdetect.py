import cv2
import numpy as np

image = cv2.imread('red.png')
cv2.imwrite('tests/red.png', image)

height = image.shape[0]
width = image.shape[1]

dimensions = (int(0.1 * width), int(0.1 * height))
scaled_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA) #INTER_LINEAR

kernel = (7,7)
sigmaX = 0
blurred = cv2.GaussianBlur(scaled_image, kernel, sigmaX)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# print(hsv)

lower_red1 = np.array([0, 100, 30])
upper_red1 = np.array([20, 255, 255])

lower_red2 = np.array([160, 100, 30])
upper_red2 = np.array([179, 255, 255])

mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)


cmask = cv2.bitwise_or(mask1, mask2)

maxy = np.argmax(cmask[0])

contours = cv2.findContours(cmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #CHAIN_APPROX_NONE

if contours:
    # print(contours)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    origin = (x, y)
    endpoint = (x + w, maxy)
    cv2.rectangle(scaled_image, origin, endpoint, (255, 0, 0), 2)
else:
    # raise Exception("no contours")
    pass


# ! tests
cv2.imwrite("tests/blur.png", blurred)
cv2.imwrite("tests/hsv.png", hsv)
# cv2.imwrite("tests/mask1.png", mask1)
# cv2.imwrite("tests/mask2.png", mask2)
cv2.imwrite("tests/cmask.png", mask2)

# ! result
cv2.imwrite('tests/processed_red.png', scaled_image)