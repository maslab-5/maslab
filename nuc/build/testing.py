import time
from camera import Camera
import cv2
import numpy as np
from visual import Visual

preBlur = 9
postBlur = 7
resizeWidth = 256
resizeHeight = 192

green_range = [[40, 20, 20], [90, 255, 255]]
red_range = [[-10, 120, 70], [10, 255, 255]]

approach_thresh = 30
angle_thresh = 20
camera_bias = 10

maxFPS = 30

# map = Map("2024_mock_comp_1.txt")
camera = Camera(0, resizeWidth, resizeHeight, preBlur, postBlur)
vis = Visual(camera, -10, green_range, red_range)
# command = Com(115200)

while True:
    img = camera.getHSVImage()
    mask = vis.applyFilter(img, green_range)
    cv2.waitKey(1)
    cv2.imshow("", mask)
    cv2.waitKey(1)
    time.sleep(0.1)



# command.setMotorEnable(LargeMotor.Chute, 1)
# command.setMotorCurrent(LargeMotor.Chute, 100)
# command.setMotorDirection(LargeMotor.Chute, 0)
# command.setMotorEnable(LargeMotor.Lift, 1)
# command.setMotorCurrent(LargeMotor.Lift, 40)
# command.setParameters(0.4, 0.0005)
# command.setOrigin(0, 0, 0)
# command.motorMove(SmallMotor.Chute, 100, 0)

# time.sleep(2)
# dir = 1
# while True:
#     command.setMotorDirection(LargeMotor.Lift, dir)
#     while command.getSwitch(4):
#         time.sleep(0.1)
#     while not command.getSwitch(4):
#         time.sleep(0.1)

#     command.setMotorSpeed(LargeMotor.Lift, 50)

#     while command.getSwitch(4):
#         time.sleep(0.1)
#     while not command.getSwitch(4):
#         time.sleep(0.1)
    
#     command.setMotorSpeed(LargeMotor.Lift, 0)
#     dir = not dir
# time.sleep(4)
# command.setMotorSpeed(LargeMotor.Chute, 0)

    

# command.setMotorSpeed(LargeMotor.Lift, 0)
# command.motorMove(SmallMotor.Chute, 0, 0)

# command.setMotorSpeed(LargeMotor.Chute, 0)

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
