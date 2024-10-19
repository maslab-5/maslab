from enum import Enum
import serial
import glob
import cv2
import numpy as np
import time
import sys

mapfile = "2024_mock_comp_1.txt"
visionFPS = 20
preBlur = 3
postBlur = 3
resizeWidth = 256
resizeHeight = 256
partialPercentThreshold = 0.1

#hsv
green_range = [[35, 20, 20], [90, 255, 255]]
red_range = [[-10, 120, 70], [10, 255, 255]]

###########################################
partialPixelsThreshold = partialPercentThreshold*resizeWidth*resizeHeight

filter_ranges = [green_range, red_range]


def addCube(x, y, height, isRed):
    index = -1
    for i in range(len(stacks)):
        stack = stacks[i]
        if stack[0] == x and stack[1] == y:
            index = i
    
    if index == -1:
        stacks.append([x, y, [0, 0, 0]])

    stacks[index][2][height] = isRed

#read map


#invert y coordinates


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

#start camera
cap = cv2.VideoCapture(0)
#start serial
ports = glob.glob('/dev/tty[A-Za-z]*')
if len(ports) == 0:
    sys.exit(0)

print(ports)
ser = serial.Serial(port=ports[0],baudrate=115200)

def sendData(values):
    ser.write(values)
    return ser.read(2)

def delay(sec):
    time.sleep(sec)

def cameraImg():
    ret, img = cap.read()
    if not ret:
        sys.exit(0)

    img = cv2.GaussianBlur(img, (preBlur, preBlur), 0)
    img = cv2.resize(img, (resizeWidth, resizeHeight))
    img = cv2.GaussianBlur(img, (postBlur, postBlur), 0)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return hsv;

def applyFilter(img, filter):
    if filter[0][0] < 0:
        filter1 = [filter[0].copy(), filter[1].copy()]
        filter2 = [filter[0].copy(), filter[1].copy()]

        filter1[0][0] = 0
        filter2[0][0] += 180
        filter2[1][0] = 180

        mask1 = cv2.inRange(img, np.array(filter1[0]), np.array(filter1[1]))
        mask2 = cv2.inRange(img, np.array(filter2[0]), np.array(filter2[1]))
        return cv2.bitwise_or(mask1, mask2)
    else:
        return cv2.inRange(img, np.array(filter[0]), np.array(filter[1]))

def isTopColor(img, isRed):
    filter_range = filter_ranges[isRed]
    mask = applyFilter(img, filter_range)
    return np.sum(mask) > partialPixelsThreshold

def getAngle(img, isRed):
    #-45 to 45
    #TODO
    return False
    ...

def reorient(angle):
    #moves to fix angle difference
    ...

def collect(stackIndex):
    collectStack = stacks[stackIndex]
    topColorRed = collectStack[2][2]

    # cameraSevo -> 0
    sendData([0, 0, 0, 0])
    delay(0.5)

    # drive fast 1000
    sendData([0, 1, 0, 0, 0, 0x03, 0xE8])
    while True:
        if isTopColor(cameraImg(), topColorRed):
            break

        delay(1/visionFPS)

    #drive slow 500
    delay(0.2)
    
    angle = getAngle(cameraImg(), topColorRed)
    if abs(angle) > 20:
        sendData([0, 2])
        delay(1)
        reorient(angle)

    delay(0.5)
    sendData([0, 2])
    delay(0.1)


    #clamp close
    sendData([0, 3, 0, 100, 0])
    delay(2)
    sendData([0, 3, 0, 0, 0])

    for i in range(3):
        #clasp servo up
        sendData([0, 3, 1, 50, 0])

        if collectStack[2][i] == primaryRed:
            #pivot on right wheel, 360 degrees
            sendData([0, 1, 2, 0, 0x03, 0xE8])
            #primary
            ...
        else:
            #pivot on left wheel, 360 degrees
            sendData([0, 1, 2, 1, 0x03, 0xE8])
            #secondary
            ...

        #clasp servo down
        delay(1)