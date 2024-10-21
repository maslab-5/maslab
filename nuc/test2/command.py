import serial
import sys
import glob
import struct
from enum import Enum

class Movement(Enum):
    Line = 0
    Spin = 1
    PivotLeft = 2
    PivotRight = 3

class Motor(Enum):
    Left = 0
    Right = 1
    Chute = 2

class SmallMotor(Enum):
    GateMotor = 0

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

    def unpack16(self, value):
        data = struct.pack('<H', value)
        return struct.unpack('<BB', data)
    
    def unpack32(self, value):
        data = struct.pack('<i', value)
        return struct.unpack('<BBBB', data)

    def unpackf(self, value):
        data = struct.pack('f', value)
        return struct.unpack('<BBBB', data)
    
    def packf(self, bytes):
        return struct.unpack('f', bytes)[0]

    def moveCamera(self, value):
        b1, b2 = self.unpack16(value)
        self.sendData(bytearray([0, 0, b1, b2]), 1)

    def startMovement(self, movement, amount):
        b1, b2, b3, b4 = self.unpack32(amount)
        self.sendData(bytearray([1, movement.value, b1, b2, b3, b4]), 1)

    def setParameters(self, ret, accel, speed):
        b1, b2, b3, b4 = self.unpackf(accel)
        b5, b6, b7, b8 = self.unpackf(speed)
        self.sendData(bytearray([2, ret, b1, b2, b3, b4, b5, b6, b7, b8]), 1)

    def motorMove(self, motor, pwmA, pwmB):
        self.sendData(bytearray([3, motor.value, pwmA, pwmB]), 1)

    def setMotorEnable(self, motor, enable):
        self.sendData(bytearray([4, motor.value, enable]), 1)
    
    def setMotorCurrent(self, motor, current):
        self.sendData(bytearray([5, motor.value, current]), 1)
    
    def setMotorDirection(self, motor, direction):
        self.sendData(bytearray([6, motor.value, direction]), 1)
    
    def setMotorSpeed(self, motor, speed):
        self.sendData(bytearray([7, motor.value, speed]), 1)

    def isMoving(self):
        return self.sendData(bytearray([8]), 2)[1]
    
    def getPosition(self):
        bytes = self.sendData(bytearray([10]), 13)
        # Ensure you extract the correct slices from the bytearray
        posx_bytes = bytes[1:5]
        posy_bytes = bytes[5:9]
        bearing_bytes = bytes[9:13]
        # Use the packf function to convert byte arrays to floats
        posx = self.packf(posx_bytes)
        posy = self.packf(posy_bytes)
        bearing = self.packf(bearing_bytes)

        return posx, posy, bearing