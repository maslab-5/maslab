import numpy as np
import cv2

def greenMask(hsv):
    # Define a range for green color in HSV
    lower_green = np.array([35, 20, 20])
    upper_green = np.array([90, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_mask = np.float32(green_mask)

    # Perform erosion to remove small white regions
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(green_mask, kernel, iterations=3)

    # Perform dilation to bring back the original size of the white regions
    processed_green_mask = cv2.dilate(erosion, kernel, iterations=5)
    processed_green_mask = processed_green_mask.astype(np.uint8)

    return processed_green_mask

def redMask(hsv):
    # Define a range for red color in HSV
    # 150 to 180
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    red_mask_1 = cv2.inRange(hsv, lower_red, upper_red)

    # 0 to 30
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([20, 255, 255])
    red_mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    # Combine masks
    red_mask = cv2.bitwise_or(red_mask_1, red_mask_2)
    red_mask = np.float32(red_mask)

    # Perform erosion to remove small white regions
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(red_mask, kernel, iterations=4)

    # Perform dilation to bring back the original size of the white regions
    processed_red_mask = cv2.dilate(erosion, kernel, iterations=4)
    processed_red_mask = processed_red_mask.astype(np.uint8)

    return processed_red_mask
