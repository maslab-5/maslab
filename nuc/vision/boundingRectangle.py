import cv2
import numpy as np


def process_frame(image):
    height, width = image.shape[:2]
    offset = 0

    dimensions = (int(0.2 * width), int(0.2 * height))
    scaled_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
    center = scaled_image.shape[1] / 2

    kernel = (7, 7)
    sigmaX = 0
    blurred = cv2.GaussianBlur(scaled_image, kernel, sigmaX)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    combined_mask = cv2.bitwise_or(mask_red, mask_green)
    contours = cv2.findContours(
        combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )[0]

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        origin = (x, y)
        endpoint = (x + w, y + h)
        rect_center = x + w // 2
        offset = int(rect_center - center)
        cv2.rectangle(scaled_image, origin, endpoint, (255, 0, 0), 2)

    return (scaled_image, offset)


cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('img/1.mov')
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))

while True:
    # while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = process_frame(frame)
    out.write(processed_frame[0])

    cv2.imshow("frame", processed_frame[0])
    # print(processed_frame[1])
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
