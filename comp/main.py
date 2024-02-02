from map import Map
from camera import Camera
from command import Com, SmallMotor, LargeMotor, Servo, Switch, Movement
from actions import Actions
from visual import Visual

import time
import os

running_nuc = os.name != 'nt'

preBlur = 9
postBlur = 7
resizeWidth = 256
resizeHeight = 192

green_range = [[35, 20, 20], [90, 255, 255]]
red_range = [[-10, 120, 70], [10, 255, 255]]

unitLength = 1452
unitRotation = 1575

camera_index = 1
if running_nuc:
    camera_index = 0

camera_bias_x = -8

# roughStartX = 0.63
# roughStartY = 4.25
roughStartX = 5
roughStartY = 3

stackOrder = [0, 1, 2, 3, 4]
maxLoop = 20

map = Map("mapgen.txt", roughStartX, roughStartY)
camera = Camera(camera_index, resizeWidth, resizeHeight, preBlur, postBlur)
command = Com(115200)
visual = Visual(camera, camera_bias_x, green_range, red_range)
act = Actions(map, command, visual, unitLength, unitRotation, maxLoop)

def init():
    command.startGyroCal(5000)
    while not command.isGyroCal():
        time.sleep(1/maxLoop)

    command.setPosition(map.roughStartX*unitLength, map.roughStartY*unitLength, map.startAng)

    command.setMotorEnable(LargeMotor.Chute, 1)
    command.setMotorDirection(LargeMotor.Chute, 1)
    command.setMotorCurrent(LargeMotor.Chute, 100)

    command.setParameters(0.2, 0.00075)

    command.moveServo(Servo.Camera, 250)
    command.moveServo(Servo.Gate, 400)
    command.moveServo(Servo.LeftChute, 50)
    command.moveServo(Servo.RightChute, 520)

    command.motorMove(SmallMotor.GateMotor, 0, 100)
    command.motorMove(SmallMotor.LiftMotor, 0, 100)
    command.setMotorSpeed(LargeMotor.Chute, 100)

    time.sleep(1)

    command.motorMove(SmallMotor.GateMotor, 0, 0)
    command.motorMove(SmallMotor.LiftMotor, 0, 0)

    command.setMotorDirection(LargeMotor.Chute, 0)
    while not command.getSwitch(Switch.ChuteLimit):
        time.sleep(1/maxLoop)

    command.setMotorSpeed(LargeMotor.Chute, 0)
    command.setMotorDirection(LargeMotor.Chute, 1)


init()

# act.turnToStack(Movement.PivotLeft, stackOrder[0])
# act.moveUptoStack(stackOrder[0])
# while command.isMoving():
#     time.sleep(1/maxLoop)
# act.alignCamera()
# act.grabStack()
# act.sortStack()

# act.turnToStack(Movement.PivotLeft, stackOrder[1])
# act.moveUptoStack(stackOrder[1])
# # act.alignCamera()
# # act.grabStack()
# # act.sortStack()

# act.turnToStack(Movement.PivotRight, stackOrder[2])
# act.moveUptoStack(stackOrder[2])
# # act.lignCamera()
# # act.grabStack()
# # act.sortStack()

# act.turnToStack(Movement.PivotLeft,stackOrder[3])
# act.moveUptoStack(stackOrder[3])
# # act.alignCamera()
# # act.grabStack()
# # act.sortStack()

# act.turnToStack(Movement.PivotLeft, stackOrder[4])
# act.moveUptoStack(stackOrder[4])
# act.alignCamera()
# act.grabStack()
# act.sortStack()

# #drop off small stack
# act.turnToPositionNearest(Movement.Spin, 4.5, 4)
# act.moveToPosition(4.5, 4, 1)
# act.turnToPositionNearest(Movement.Spin, 3, 4)
# act.dropGround()

command.setParameters(0.2, 0.00075)
act.turnToPositionNearest(Movement.Spin, 3.5, 4.25)
command.setParameters(0.5, 0.00075)
act.moveToPosition(3.5, 4.25, 1)
command.setParameters(0.2, 0.00075)
act.turnToPositionNearest(Movement.Spin, 3.5, 2)
act.dropPlatform()

camera.destroy()
