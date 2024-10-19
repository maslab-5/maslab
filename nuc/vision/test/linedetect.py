import cv2
import numpy as np

image = cv2.imread('GroundWithPlatform.png')

# Scale the image to 10%
height, width = image.shape[:2]

scaled_image = cv2.GaussianBlur(image, (21, 21), 0)

scaled_image = cv2.resize(scaled_image, (int(0.2 * width), int(0.2 * height)))

scaled_image = cv2.GaussianBlur(scaled_image, (5, 5), 0)

# Convert the scaled image to the HSV color space
hsv_image = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2HSV)

# Define a range for blue color in HSV
lower_blue = np.array([100, 80, 80])
upper_blue = np.array([140, 255, 255])

# Create a mask for blue pixels
blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

im_floodfill = blue_mask.copy()
h, w = blue_mask.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

#pick this position better
cv2.floodFill(im_floodfill, None, (0,0), 255)

im_floodfill = np.bitwise_not(im_floodfill)

hsv_fill = np.where(im_floodfill[:, :, None], hsv_image, 0)

original = cv2.cvtColor(hsv_fill.astype(np.uint8), cv2.COLOR_HSV2BGR)

cv2.imshow('Original Image', original)

# blue_mask = np.uint8(blue_mask)
# # Make only the pixels above the blue mask black
# result_image = cv2.bitwise_and(image, image, mask=blue_mask)

# # Display the original image, blue mask, and result image
# cv2.imshow('Original Image', image)
# cv2.imshow('Blue Mask', blue_mask)
# cv2.imshow('Result Image', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()