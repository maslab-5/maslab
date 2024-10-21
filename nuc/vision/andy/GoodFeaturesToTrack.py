import numpy as np
import cv2

# Load image
img = cv2.imread('GreenRedGreen.png')

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define a range for green color in HSV
lower_green = np.array([40, 00, 00])
upper_green = np.array([80, 255, 255])
green_mask = cv2.inRange(hsv, lower_green, upper_green)
green_mask = np.float32(green_mask)

# Perform erosion to remove small white regions
kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(green_mask, kernel, iterations=2)

# Perform dilation to bring back the original size of the white regions
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))
processed_green_mask = cv2.dilate(erosion, kernel, iterations=7)

# Blur
# processed_green_mask = cv2.GaussianBlur(processed_green_mask, (51, 51), 1)

# Detect corners using Shi-Tomasi algorithm
corners = cv2.goodFeaturesToTrack(processed_green_mask, maxCorners=16, qualityLevel=0.01, minDistance=500)

# Convert corners to integer coordinates
corners = np.int0(corners)

# Draw circles around detected corners
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y),10, 255, -1)

# Display the result
cv2.imshow('Original Mask', green_mask)
cv2.imshow('Processed Mask', processed_green_mask)
cv2.imshow('Original Image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
