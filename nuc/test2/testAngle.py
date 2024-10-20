import time
from camera import Camera
from command import Com
from command import Movement
from command import Motor
from command import SmallMotor
from map import Map
import cv2
import numpy as np

preBlur = 9
postBlur = 7
resizeWidth = 256
resizeHeight = 192

green_range = [[35, 20, 20], [90, 255, 255]]
red_range = [[-10, 120, 70], [10, 255, 255]]
filters = [green_range, red_range]

approach_thresh = 30
angle_thresh = 20
camera_bias = 10

maxFPS = 30

map = Map("2024_mock_comp_1.txt")
camera = Camera(1, (resizeWidth, resizeHeight), preBlur, postBlur, filters[map.primaryRed], filters[not map.primaryRed])
command = Com(115200)

time.sleep(0.1)

command.setMotorEnable(Motor.Left, 1)
command.setMotorEnable(Motor.Right, 1)
command.setMotorEnable(Motor.Chute, 1)
command.setMotorCurrent(Motor.Left, 50)
command.setMotorCurrent(Motor.Right, 50)
command.setMotorCurrent(Motor.Chute, 20)

time.sleep(0.1)

command.moveCamera(200)

time.sleep(1)
# command.startMovement(Movement.Spin, 1, 0, 200)

# while True:
#     img = camera.getImage()

#     time.sleep(1/maxFPS)


while True:
    img = camera.getImage()
    mask = camera.applyFilter(camera.toHSV(img), green_range)
    coords = np.column_stack(np.where(mask))
    median_x = np.median(coords[:, 1])
    offset = median_x-resizeWidth/2+camera_bias

    print(offset)

    scale = 0.6

    amount = offset
    dir = 1
    if offset < 0:
        amount = -offset
        dir = 0

    amount *= scale

    command.startMovement(Movement.Spin, dir, 0, int(amount))

    while command.isMoving():
        time.sleep(0.05)

    cv2.waitKey(1)
    cv2.imshow("feed", mask)
    cv2.waitKey(1)
    time.sleep(1/maxFPS)