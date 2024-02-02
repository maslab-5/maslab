import time
from camera import Camera
from command import Com
from command import Movement
from command import Motor
from command import SmallMotor
from map import Map
import cv2

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

maxFPS = 30

map = Map("2024_mock_comp_1.txt", unitLength)
camera = Camera(1, (resizeWidth, resizeHeight), preBlur, postBlur, filters[map.primaryRed], filters[not map.primaryRed])
command = Com(115200)

time.sleep(0.1)

command.setMotorEnable(Motor.Chute, 1)
command.setMotorCurrent(Motor.Chute, 20)

time.sleep(0.1)

command.moveCamera(0)
command.motorMove(SmallMotor.GateMotor, 0, 100)
command.moveGate(400)
command.setParameters(0.2, 0.0008)

time.sleep(1)

command.motorMove(SmallMotor.GateMotor, 0, 0)
command.startMovement(Movement.Line, 1500)
# command.setMotorDirection(Motor.Chute, 0)
# command.setMotorSpeed(Motor.Chute, 100)
# command.motorMove(SmallMotor.GateMotor, 0, 100)

# command.setMotorSpeed(Motor.Chute, 0)
# command.stopMovement()
# command.motorMove(SmallMotor.GateMotor, 0, 0)
# print(command.isMoving())

while True:
    percent = camera.getPercentFilter(filters[not map.primaryRed])
    # print(percent)
    if percent > approach_thresh:
        command.setParameters(0.1, 0.001)
        command.startMovement(Movement.Line, 275)
        break

    time.sleep(1/maxFPS)

time.sleep(0.5)

angle = camera.getAngle()
if angle > angle_thresh:
    #readjust routine
    ...

# command.startMovement(Movement.Line, 0, 0, 275)
while command.isMoving():
    time.sleep(0.1)

command.motorMove(SmallMotor.GateMotor, 100, 0)
time.sleep(1)
command.motorMove(SmallMotor.GateMotor, 0, 0)
# while True:
#     img = camera.getImage()
#     cv2.waitKey(1)
#     cv2.imshow("feed", img)
#     cv2.waitKey(1)