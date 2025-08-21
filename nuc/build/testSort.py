import time
from camera import Camera
from command import Com
from command import Movement
from command import Motor
from command import SmallMotor
from command import Servo
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

# map = Map("2024_mock_comp_1.txt")
# camera = Camera(1, (resizeWidth, resizeHeight), preBlur, postBlur, filters[map.primaryRed], filters[not map.primaryRed])
command = Com(115200)

time.sleep(0.1)

command.setMotorEnable(Motor.Left, 1)
command.setMotorEnable(Motor.Right, 1)
command.setMotorEnable(Motor.Chute, 1)
command.setMotorCurrent(Motor.Left, 50)
command.setMotorCurrent(Motor.Right, 50)
command.setMotorCurrent(Motor.Chute, 10)

time.sleep(0.1)

command.moveCamera(0)
command.moveGate(0)

# command.moveServo(Servo.LeftChute, 550)#open
command.moveServo(Servo.LeftChute, 45)#close

# command.moveServo(Servo.RightChute, 0)#open
command.moveServo(Servo.RightChute, 550)#close

command.setParameters(0, 0.0015, 0.4)
command.setMotorDirection(Motor.Chute, 0)

command.startMovement(Movement.PivotRight, 360*8)

time.sleep(0.9)

command.moveGate(400)

while command.isMoving():
    time.sleep(0.2)


# # command.startMovement(Movement.Line, 2000)
# # while command.isMoving():
# #     time.sleep(0.05)
# # time.sleep(0.5)
# time.sleep(1)

# command.setMotorSpeed(Motor.Chute, 0)

# command.startMovement(Movement.Line, 1000)
# while command.isMoving():
#     time.sleep(0.05)
# time.sleep(0.5)


# while True:
#     img = camera.getImage()

#     time.sleep(1/maxFPS)
