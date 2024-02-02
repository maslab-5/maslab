import cv2
import numpy as np

def wallDetect(image):
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
    h, w = blue_mask.shape
    # mask = np.zeros((h+2, w+2), np.uint8)

    #pick this position better
    cv2.floodFill(im_floodfill, None, (0,0), 255)

    im_floodfill = np.bitwise_not(im_floodfill)

    hsv_fill = np.where(im_floodfill[:, :, None], hsv_image, 0)

    original = cv2.cvtColor(hsv_fill.astype(np.uint8), cv2.COLOR_HSV2BGR)

    return original

cap = cv2.VideoCapture('Videos/IMG_6317.mp4')

# while True:
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = wallDetect(frame)
    
    cv2.imshow('frame', processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
