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
    erosion = cv2.erode(green_mask, kernel, iterations=2)

    # Perform dilation to bring back the original size of the white regions
    processed_green_mask = cv2.dilate(erosion, kernel, iterations=2)
    processed_green_mask = processed_green_mask.astype(np.uint8)

    return processed_green_mask

def redMask(hsv):
    # Define a range for red color in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    red_mask_1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask_2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine masks
    red_mask = cv2.bitwise_or(red_mask_1, red_mask_2)
    red_mask = np.float32(red_mask)

    # Perform erosion to remove small white regions
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(red_mask, kernel, iterations=2)

    # Perform dilation to bring back the original size of the white regions
    processed_red_mask = cv2.dilate(erosion, kernel, iterations=2)
    processed_red_mask = processed_red_mask.astype(np.uint8)

    return processed_red_mask

def approxPolyDP(img):
    # Load and blur image
    height, width = img.shape[:2]
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.resize(img, (int(0.5 * width), int(0.5 * height)))
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get masks
    processed_green_mask = greenMask(hsv)
    processed_red_mask = redMask(hsv)

    # Get and combine contours
    green_contours, _ = cv2.findContours(processed_green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    red_contours, _ = cv2.findContours(processed_red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = green_contours + red_contours

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.arcLength(largest_contour, closed=True) > 300:
            approx = cv2.approxPolyDP(largest_contour, 0.02 * cv2.arcLength(largest_contour, True), True)
            rect = cv2.minAreaRect(approx)
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            angle = rect[-1]

            print (angle)
            cv2.drawContours(img, [approx], 0, (0, 255, 0), 10)

    return img

# Video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = approxPolyDP(frame)

cap.release()
cv2.destroyAllWindows()
