import time
from camera import Camera
from command import Com
from command import Movement
from command import Motor
from command import SmallMotor
from map import Map
import cv2
import math
import numpy as np

preBlur = 9
postBlur = 7
resizeWidth = 256
resizeHeight = 192

green_range = [[35, 20, 20], [90, 255, 255]]
red_range = [[-10, 120, 70], [10, 255, 255]]
filters = [green_range, red_range]

unitLength = 1452
rough_approach_dist = 500
approach_thresh = 30
angle_thresh = 10

camera_bias_x = 10

maxFPS = 30

map = Map("2024_mock_comp_1.txt", unitLength)
camera = Camera(1, (resizeWidth, resizeHeight), preBlur, postBlur, filters[map.primaryRed], filters[not map.primaryRed])
command = Com(115200)

time.sleep(0.1)

command.setOrigin(map.startX, map.startY, map.startAng)
command.setMotorEnable(Motor.Chute, 1)
command.setMotorCurrent(Motor.Chute, 30)
command.setParameters(0.4, 0.0004)

time.sleep(0.1)

command.moveCamera(400)
command.moveGate(0)
command.motorMove(SmallMotor.GateMotor, 0, 100)

time.sleep(1)

command.motorMove(SmallMotor.GateMotor, 0, 0)
#1575
command.startMovement(Movement.Line, -200)

# for collect in range(5):
#     robX, robY, robBear = command.getPosition()
#     print(robX, robY, robBear)
#     blockIndex, dist = map.nearestCube(robX, robY)
#     print(blockIndex)
#     rotate = map.angleTo(robX, robY, robBear, blockIndex)
#     print(rotate)
#     command.startMovement(Movement.Spin, int(rotate/math.pi*2*366))
#     while command.isMoving():
#         time.sleep(0.1)

#     command.startMovement(Movement.Line, max(int(dist-rough_approach_dist), 0))
#     while command.isMoving():
#         time.sleep(0.1)

#     time.sleep(1)
