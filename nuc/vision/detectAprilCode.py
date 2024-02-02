import numpy as np
import cv2
from pupil_apriltags import Detector

at_detector = Detector(
   families="tag36h11",
   nthreads=1,
   quad_decimate=3,
   quad_sigma=0.2,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0
)

def aprilCode(img):
    # Detect tags
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tags = at_detector.detect(
            gray_img,
            estimate_tag_pose=False,
            camera_params=None,
            tag_size=None,
        )

    #Using corners of each tag to draw lines
    for tag in tags:
        corners = tag.corners
        corner_01 = (int(corners[0][0]), int(corners[0][1]))
        corner_02 = (int(corners[1][0]), int(corners[1][1]))
        corner_03 = (int(corners[2][0]), int(corners[2][1]))
        corner_04 = (int(corners[3][0]), int(corners[3][1]))

        cv2.line(img, (corner_01[0], corner_01[1]),
                (corner_02[0], corner_02[1]), (0, 255, 255), 2)
        cv2.line(img, (corner_02[0], corner_02[1]),
                (corner_03[0], corner_03[1]), (0, 255, 255), 2)
        cv2.line(img, (corner_03[0], corner_03[1]),
                (corner_04[0], corner_04[1]), (0, 255, 255), 2)
        cv2.line(img, (corner_04[0], corner_04[1]),
                (corner_01[0], corner_01[1]), (0, 255, 255), 2)

    return img


cap = cv2.VideoCapture('Videos/IMG_3756.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = aprilCode(frame)

    cv2.imshow("Frame", processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
