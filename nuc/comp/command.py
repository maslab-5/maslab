import serial
import sys
import glob
import struct
from enum import Enum
import math

class Servo(Enum):
    Camera = 0
    Gate = 1
    LeftChute = 2
    RightChute = 3

class Movement(Enum):
    Line = 0
    Spin = 1
    PivotLeft = 2
    PivotRight = 3
    ArcLeft = 4
    ArcRight = 5

class LargeMotor(Enum):
    Left = 0
    Right = 1
    Chute = 2
    Lift = 3

class SmallMotor(Enum):
    Gate = 0

class Switch(Enum):
    UserTop = 4
    ChuteLimit = 5

def getBytes16(value):
    data = struct.pack('<H', value)
    return struct.unpack('<BB', data)

def getBytes32(value):
    data = struct.pack('<i', value)
    return struct.unpack('<BBBB', data)

def getBytesf(value):
    data = struct.pack('f', value)
    return struct.unpack('<BBBB', data)

def fromBytesf(bytes):
    return struct.unpack('f', bytes)[0]

class Com:
    def __init__(self, baud):
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
        
        self.port = result[0]
        self.ser = serial.Serial(port=self.port,baudrate=baud)

    def sendData(self, barray, listen_len):
        self.ser.write(barray)
        return self.ser.read(listen_len)
    
    def sendCommand(self, command, data):
        self.sendData(bytearray([command] + data), 1)

    def recieveCommand(self, command, data, resp_len):
        return self.sendData(bytearray([command] + data), resp_len)
    
    def boolResponse(self, command, data):
        return self.recieveCommand(command, data, 2)[1]

    def moveServo(self, servo, pos):
        b1, b2 = getBytes16(pos)
        self.sendCommand(0, [servo.value, b1, b2])

    def startMovement(self, movement, amount):
        b1, b2, b3, b4 = getBytes32(amount)
        self.sendCommand(1, [movement.value, b1, b2, b3, b4])

    def setParameters(self, speed, accel):
        b1, b2, b3, b4 = getBytesf(speed)
        b5, b6, b7, b8 = getBytesf(accel)
        self.sendCommand(2, [b1, b2, b3, b4, b5, b6, b7, b8])

    def motorMove(self, motor, pwmA, pwmB):
        self.sendCommand(3, [motor.value, pwmA, pwmB])

    def setMotorEnable(self, motor, enable):
        self.sendCommand(4, [motor.value, enable])
    
    def setMotorCurrent(self, motor, current):
        self.sendCommand(5, [motor.value, current])
    
    def setMotorDirection(self, motor, direction):
        self.sendCommand(6, [motor.value, direction])
    
    def setMotorSpeed(self, motor, speed):
        self.sendCommand(7, [motor.value, speed])

    def isMoving(self):
        return self.boolResponse(8, [])
    
    def getSwitch(self, switch):
        return self.boolResponse(9, [switch.value])

    def getPosition(self):
        bytes = self.recieveCommand(10, [], 13)
        
        posx = fromBytesf(bytes[1:5])
        posy = fromBytesf(bytes[5:9])
        bearing = fromBytesf(bytes[9:13])

        return posx, posy, bearing
    
    def setPosition(self, x, y, ang):
        b1, b2, b3, b4 = getBytesf(x)
        b5, b6, b7, b8 = getBytesf(y)
        b9, b10, b11, b12 = getBytesf(ang)

        self.sendCommand(11, [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12])

    def stopMovement(self):
        self.sendCommand(12, [])

    def startGyroCal(self, millis):
        b1, b2 = getBytes16(millis)
        self.sendCommand(13, [b1, b2])
    
    def isGyroCal(self):
        return self.boolResponse(14, [])
    
    def clampAngle(self):
        x, y, ang = self.getPosition()
        while ang < 0:
            ang += 2*math.pi
        
        while ang >= 2*math.pi:
            ang -= 2*math.pi
        
        self.setPosition(x, y, ang)
    
    def resetPID(self):
        self.sendCommand(15, [])
