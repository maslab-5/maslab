import time
from camera import Camera
from command import Com
from command import Movement
from command import SmallMotor
from map import Map
import numpy as np

preBlur = 9
postBlur = 7
resizeWidth = 256
resizeHeight = 192

green_range = [[35, 20, 20], [90, 255, 255]]
red_range = [[-10, 120, 70], [10, 255, 255]]
filters = [green_range, red_range]

unitLength = 1452
spinTurn = 1575
rough_approach_dist = 600
approach_thresh = 30
angle_thresh = 10

camera_bias_x = 10

maxFPS = 30

map = Map("2024_mock_comp_1.txt", unitLength)
camera = Camera(1, (resizeWidth, resizeHeight), preBlur, postBlur, filters[map.primaryRed], filters[not map.primaryRed])
command = Com(115200)

time.sleep(0.1)

command.startGyroCal(5000)

while not command.isGyroCal():
    time.sleep(0.1)

command.setOrigin(map.startX, map.startY, map.startAng)
command.setMotorEnable(Motor.Chute, 1)
command.setMotorCurrent(Motor.Chute, 30)
command.setParameters(0.5, 0.0005)

time.sleep(0.1)

command.moveCamera(400)
command.moveGate(0)
command.motorMove(SmallMotor.GateMotor, 0, 100)

time.sleep(1)

command.motorMove(SmallMotor.GateMotor, 0, 0)

# command.startMovement(Movement.Line, 0, 0, 1000)
# command.setMotorDirection(Motor.Chute, 0)
# command.setMotorSpeed(Motor.Chute, 100)
# command.motorMove(SmallMotor.GateMotor, 0, 100)

# command.setMotorSpeed(Motor.Chute, 0)
# command.stopMovement()
# command.motorMove(SmallMotor.GateMotor, 0, 0)
# print(command.isMoving())

def closeApproachGrab():
    while True:
        percent = camera.getPercentFilter(filters[not map.primaryRed])
        if percent > approach_thresh:
            command.stopMovement()
            break

        time.sleep(1/maxFPS)

    time.sleep(0.5)

    angle = camera.getAngle()
    if angle > angle_thresh:
        #readjust routine
        #just rotate honestly
        ...

    command.startMovement(Movement.Line, 0, 0, 275)
    while command.isMoving():
        time.sleep(0.05)

    command.motorMove(SmallMotor.GateMotor, 100, 0)
    time.sleep(1)
    command.motorMove(SmallMotor.GateMotor, 0, 0)

def cameraAlignRoutine():
    for x in range(6):
        img = camera.getImage()
        mask = camera.applyFilter(camera.toHSV(img), green_range)
        coords = np.column_stack(np.where(mask))
        median_x = np.median(coords[:, 1])
        offset = median_x-resizeWidth/2+camera_bias_x

        command.startMovement(Movement.Spin, int(offset*0.6))

        while command.isMoving():
            time.sleep(0.05)

def collectShute():
    ...

def blockRoutine():
    cameraAlignRoutine()
    closeApproachGrab()
    collectShute()

# robX, robY, robBear = command.getPosition()
# robX += map.startX
# robY += map.startY
# robBear += map.startAng
# blockIndex, dist = map.nearestCube(robX, robY)
# rotate = map.angleTo(robX, robY, robBear, blockIndex)
# command.startMovement(Movement.Spin, int(rotate/math.pi/2*366)+turn_extra)
# while command.isMoving():
#     time.sleep(0.1)

# time.sleep(0.5)

# command.startMovement(Movement.Line, max(int(dist-rough_approach_dist), 0))
# while command.isMoving():
#     time.sleep(0.1)

# time.sleep(0.5)

for collect in range(5):
    robX, robY, robBear = command.getPosition()
    print(robX, robY, robBear)
    blockIndex, dist = map.nearestCube(robX, robY)
    print(blockIndex)
    rotate = map.angleTo(robX, robY, robBear, blockIndex)
    newAng = robBear + rotate
    
    command.gyroTurn(newAng)

    command.startMovement(Movement.Line, max(int(dist-rough_approach_dist), 0))
    while command.isMoving():
        time.sleep(0.1)

    time.sleep(1)

    # command.startMovement(Movement.Spin, int(rotate/math.pi/4*366))

    # while command.isMoving():
    #     time.sleep(0.01)

    # time.sleep(0.3)

    # command.startMovement(Movement.Line, int(max(dist - rough_approach_dist, 0)))

    # blockRoutine()

    



# while True:
#     percent = camera.getPercentFilter(filters[not map.primaryRed])
#     if percent > approach_thresh:
#         command.stopMovement()
#         break

#     time.sleep(1/maxFPS)

# time.sleep(0.5)

# angle = camera.getAngle()
# if angle > angle_thresh:
#     #readjust routine
#     ...

# command.startMovement(Movement.Line, 0, 0, 275)
# while command.isMoving():
#     time.sleep(0.05)

# command.motorMove(SmallMotor.GateMotor, 100, 0)
# time.sleep(1)
# command.motorMove(SmallMotor.GateMotor, 0, 0)
# while True:
#     img = camera.getImage()
#     cv2.waitKey(1)
#     cv2.imshow("feed", img)
#     cv2.waitKey(1)