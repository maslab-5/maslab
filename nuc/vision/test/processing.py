import cv2
import numpy as np
import math

# Load the image
image = cv2.imread('red.png')

# Scale the image to 10%
height, width = image.shape[:2]
scaled_image = cv2.resize(image, (int(0.1 * width), int(0.1 * height)))

scaled_image = cv2.GaussianBlur(scaled_image, (7, 7), 0)

# Convert the scaled image to the HSV color space
hsv = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2HSV)

# Define a lower and upper threshold for red color in HSV
lower_red1 = np.array([0, 100, 30])
upper_red1 = np.array([20, 255, 255])

lower_red2 = np.array([159, 100, 30])
upper_red2 = np.array([179, 255, 255])

# Create a binary mask for red regions
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

cmask = cv2.bitwise_or(mask1, mask2)
# Set the pixels in the mask to blue
scaled_image[cmask > 0] = [255, 0, 0]  # Blue color

# Find the indices where blue channel equals 255
blue_255_indices = np.where(scaled_image[:, :, 0] == 255)

# Find the pixel with the highest y-value where blue == 255
max_y_index = np.argmax(blue_255_indices[0])
min_y_index = np.argmin(blue_255_indices[0])
max_x_index = np.argmax(blue_255_indices[1])
min_x_index = np.argmin(blue_255_indices[1])

corxmin = blue_255_indices[1][min_x_index]
corymin = blue_255_indices[0][min_y_index]
corxmax = blue_255_indices[1][max_x_index]
corymax = blue_255_indices[0][max_y_index]

cv2.rectangle(scaled_image, (corxmin, corymin), (corxmax, corymax), (0, 0, 0), 2)

max_y = blue_255_indices[0][max_y_index]
max_x = blue_255_indices[1][max_y_index]

radius = 30
ang = 0

cx = max_x+radius
cy = max_y

value = scaled_image[cx, cy, 0]

while value != 255:
    cx = int(max_x+radius*math.cos(ang))
    cy = int(max_y-radius*math.sin(ang))
    
    ang+=0.01;
    
    value = scaled_image[cy, cx, 0]

endx1 = max_x+4*(cx-max_x)
endy1 = max_y+4*(cy-max_y)

cv2.line(scaled_image, (max_x, max_y), (endx1, endy1), (0, 255, 0), 3)

ang = 0

cx = max_x-radius
cy = max_y

value = scaled_image[cx, cy, 0]

while value != 255:
    cx = int(max_x-radius*math.cos(ang))
    cy = int(max_y-radius*math.sin(ang))
    
    ang+=0.01;
    
    value = scaled_image[cy, cx, 0]

endx2 = max_x+4*(cx-max_x)
endy2 = max_y+4*(cy-max_y)

cv2.line(scaled_image, (max_x, max_y), (endx2, endy2), (0, 255, 0), 3)

# Display the original image, scaled image, and the result
cv2.imshow('Red Object Detection', scaled_image)
cv2.waitKey(0)
cv2.destroyAllWindows()