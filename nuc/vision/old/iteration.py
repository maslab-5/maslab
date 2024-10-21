# from google.colab.patches import cv2_imshow

import cv2
import numpy as np

image = cv2.imread('red.png')

scale_percent = 30
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)


# gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(resized, (3, 3), 0)

blue_channel = blurred[:, :, 0]
green_channel = blurred[:, :, 1]
red_channel = blurred[:, :, 2]
mask = ((blue_channel-red_channel)^2 + (green_channel - red_channel)^2) < 120
# Optional: Create an image to visualize the mask
# This will create a white pixel wherever the condition is true
visualized_mask = np.zeros_like(blurred)
visualized_mask[mask] = [255, 0, 0]

cv2_imshow(visualized_mask)


# cv2_imshow(blurred)
# thresh = cv2.threshold(blurred, 0, 60, cv2.THRESH_BINARY)[1]

# contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# for contour in contours:
#     peri = cv2.arcLength(contour, True)
#     approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
#     if len(approx) == 4 or len(approx) == 6:
#         cv2.drawContours(resized, [approx], -1, (0, 255, 0), 3)
# cv2_imshow(resized)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# -----


# from google.colab.patches import cv2_imshow

# import cv2
# import numpy as np

# # Load the image
# image = cv2.imread('red.png')

# # Split the image into its RGB channels
# blue_channel = image[:,:,0]
# green_channel = image[:,:,1]

# # Calculate the difference between the green and blue channels
# channel_difference = cv2.subtract(blue_channel, green_channel)

# # Create an empty image with the same dimensions
# result_image = np.zeros_like(image)

# # Set the green channel of the result image to the channel difference
# result_image[:,:,1] = channel_difference

# # Display or save the result image
# cv2_imshow(result_image)

