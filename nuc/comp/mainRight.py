from map import Map
from camera import Camera
from command import Com, SmallMotor, LargeMotor, Servo, Switch, Movement
from actions import Actions
from visual import Visual

import math
import time
import os

# updating code
# git add .
# git commit -m "message"
# git push

# getting code
# cd robot/nuc-data
# git pull

running_nuc = os.name != 'nt'

preBlur = 9
postBlur = 7
resizeWidth = 256
resizeHeight = 192

green_range = [[40, 17, 17], [100, 255, 255]]
red_range = [[-10, 20, 20], [10, 255, 255]]

unitLength = 1462
unitRotation = 1575

camera_bias_x = -8

roughStartX = 4
roughStartY = 3

stackOrder = [2, 4, 3, 1, 0]

maxLoop = 24
dropTime = 150

map = Map("mapright.txt", roughStartX, roughStartY)
camera = Camera(running_nuc, resizeWidth, resizeHeight, preBlur, postBlur)
command = Com(115200)
visual = Visual(camera, camera_bias_x, green_range, red_range)
act = Actions(map, command, visual, unitLength, unitRotation, maxLoop, dropTime)

def init():
    command.startGyroCal(5000)
    while not command.isGyroCal():
        time.sleep(1/maxLoop)

    command.setPosition(map.roughStartX*unitLength, map.roughStartY*unitLength, map.startAng)

    command.setMotorEnable(LargeMotor.Lift, 1)
    command.setMotorDirection(LargeMotor.Lift, 0)
    command.setMotorCurrent(LargeMotor.Lift, 38)
    command.setMotorEnable(LargeMotor.Chute, 1)
    command.setMotorDirection(LargeMotor.Chute, 1)
    command.setMotorCurrent(LargeMotor.Chute, 100)

    command.setParameters(0.6, 0.00075)

    command.moveServo(Servo.Camera, 275)
    command.moveServo(Servo.Gate, 310)
    command.moveServo(Servo.LeftChute, 35)
    command.moveServo(Servo.RightChute, 528)

    command.motorMove(SmallMotor.Gate, 0, 100)
    command.setMotorSpeed(LargeMotor.Lift, 50)
    command.setMotorSpeed(LargeMotor.Chute, 100)

    time.sleep(1.5)

    command.motorMove(SmallMotor.Gate, 0, 0)
    command.setMotorDirection(LargeMotor.Chute, 0)
    command.setMotorDirection(LargeMotor.Lift, 0)

    time.sleep(0.25)

    command.setMotorEnable(LargeMotor.Lift, 0)
    command.setMotorSpeed(LargeMotor.Lift, 0)

    while not command.getSwitch(Switch.ChuteLimit):
        time.sleep(1/maxLoop)

    command.setMotorSpeed(LargeMotor.Chute, 0)
    command.setMotorDirection(LargeMotor.Chute, 1)


init()

act.turnToStack(Movement.Spin, stackOrder[0])
act.moveUptoStack(stackOrder[0])
act.alignCamera()
act.grabStack(stackOrder[0])
act.turnToBearingNearest(Movement.Spin, -3*math.pi/4)
act.sortStack()

act.turnToPositionNearest(Movement.Spin, 2, 2)
act.moveToPosition(2, 2, 1)
act.turnToStack(Movement.Spin, stackOrder[1])
act.moveUptoStack(stackOrder[1])
act.alignCamera()
act.grabStack(stackOrder[1])
act.turnToBearingNearest(Movement.Spin, math.pi/2)
act.sortStack()

act.turnToPositionNearest(Movement.Spin, 2, 0.95)
act.moveToPosition(2, 0.95, 1)
act.turnToStack(Movement.Spin, stackOrder[2])
act.moveUptoStack(stackOrder[2])
act.alignCamera()
act.grabStack(stackOrder[2])
act.turnToBearingNearest(Movement.Spin, math.pi/2)
act.sortStack()

# act.turnToPositionNearest(Movement.Spin, 2, 2)
# act.moveToPosition(2, 2, 1)
# act.turnToStack(Movement.Spin,stackOrder[3])
# act.moveUptoStack(stackOrder[3])
# act.alignCamera()
# act.grabStack(stackOrder[3])
# act.turnToBearingNearest(Movement.Spin, 0)
# act.sortStack()

# act.turnToPositionNearest(Movement.Spin, 1, 3)
# act.moveToPosition(1, 3, 1)
# act.turnToStack(Movement.Spin, stackOrder[4])
# act.moveUptoStack(stackOrder[4])
# act.alignCamera()
# act.grabStack(stackOrder[4])
# act.turnToBearingNearest(Movement.Spin, 0)
# act.sortStack()


act.turnToPositionNearest(Movement.Spin, 1, 1)
act.moveToPosition(1, 1, 1)
act.turnToBearingNearest(Movement.Spin, math.pi/2)
act.dropGround()

act.turnToPositionNearest(Movement.Spin, 1.5, 2.6)
act.moveToPosition(1.5, 2.6, 1)
act.turnToBearingNearest(Movement.Spin, 0)
# act.waitDrop()
act.dropPlatform()

camera.destroy()
