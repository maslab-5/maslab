import math
import time

import cv2
import numpy as np

from camera import Camera
from command import Com, Movement, SmallMotor
from map import Map

preBlur = 9
postBlur = 7
resizeWidth = 256
resizeHeight = 192

green_range = [[35, 20, 20], [90, 255, 255]]
red_range = [[-10, 120, 70], [10, 255, 255]]
filters = [green_range, red_range]

unitLength = 1452
spinTurn = 1575
approach_thresh = 30
angle_thresh = 20
camera_bias = 10

maxFPS = 30

map = Map("2024_mock_comp_1.txt", unitLength)
camera = Camera(1, (resizeWidth, resizeHeight), preBlur, postBlur, filters[map.primaryRed], filters[not map.primaryRed])
command = Com(115200)

time.sleep(0.1)

command.startGyroCal(3000)

while not command.isGyroCal():
    time.sleep(0.1)

command.setOrigin(0, 0, 0)
# command.setMotorEnable(Motor.Chute, 1)
# command.setMotorCurrent(Motor.Chute, 20)

time.sleep(0.1)

command.moveCamera(200)

time.sleep(1)
# command.startMovement(Movement.Spin, 1, 0, 200)

# while True:
#     img = camera.getImage()

#     time.sleep(1/maxFPS)

while True:
    command.gyroTurn(math.pi/2)
    time.sleep(0.1)
print("done")