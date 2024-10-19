import time

import cv2
import numpy as np

from camera import Camera
from command import Com, LargeMotor, Movement, Servo, SmallMotor
from map import Map

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

command.setMotorEnable(LargeMotor.Chute, 1)
command.setMotorCurrent(LargeMotor.Chute, 100)
command.setMotorDirection(LargeMotor.Chute, 1)
command.setParameters(0.4, 0.0005)
# command.setOrigin(0, 0, 0)
command.setMotorSpeed(LargeMotor.Chute, 100)

time.sleep(1)

while not command.getSwitch(5):
    time.sleep(0.1)

command.setMotorSpeed(LargeMotor.Chute, 0)

# time.sleep(0.5)

# print(command.getPosition())
# command.startMovement(Movement.Spin, 100)
# time.sleep(4)
# print(command.getPosition())
# command.stopMovement()
# command.startMovement(Movement.Line, 0)

# command.moveCamera(0)
# command.moveGate(0)

# command.moveServo(Servo.LeftChute, 550)#open
# command.moveServo(Servo.LeftChute, 45)#close

# command.moveServo(Servo.RightChute, 0)#open
# command.moveServo(Servo.RightChute, 550)#close

# command.setParameters(0, 0.001, 0.2)
# command.setMotorDirection(Motor.Chute, 0)

# time.sleep(1)

# command.startMovement(Movement.Line, 1000)
# time.sleep(0.5)
# command.setMotorSpeed(Motor.Chute, 100)
# time.sleep(10)
# command.setMotorSpeed(Motor.Chute, 0)

# command.setMotorSpeed(Motor.Chute, 15)

# command.setMotorSpeed(Motor.Chute, 0)
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
