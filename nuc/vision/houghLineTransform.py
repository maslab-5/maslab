import numpy as np
import cv2

# Load image
img = cv2.imread('GreenRedGreen.png')

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define a range for green color in HSV
lower_green = np.array([40, 00, 00])
upper_green = np.array([90, 255, 255])
green_mask = cv2.inRange(hsv, lower_green, upper_green)
green_mask = np.float32(green_mask)

# Perform erosion to remove small white regions
kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(green_mask, kernel, iterations=2)

# Perform dilation to bring back the original size of the white regions
processed_green_mask = cv2.dilate(erosion, kernel, iterations=64)

# Implement mask
# processed_green_mask = processed_green_mask.astype(np.uint8)
# result = cv2.bitwise_and(img, img, mask=processed_green_mask)

# Get edges
# edges = cv2.Canny(result, 100, 200, apertureSize=3)

# Hough Line
result_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
lines = cv2.HoughLinesP(result_gray, 1, np.pi / 180, threshold=1000)

# Draw Lines
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Show images
cv2.imshow('Mask',processed_green_mask)
# cv2.imshow('Gray',result_gray)
# cv2.imshow('Result',result)
# cv2.imshow('Edges',edges)
cv2.waitKey()
