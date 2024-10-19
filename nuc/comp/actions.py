from command import Movement, Servo, SmallMotor, LargeMotor, Switch

import math
import time

class Actions:
    def __init__(self, map, command, visual, unitLength, unitRotation, maxLoop, dropTime):
        self.map = map
        self.com = command
        self.vis = visual

        self.unitLength = unitLength
        self.unitRotation = unitRotation

        self.maxLoop = maxLoop
        self.startTime = time.time()
        self.dropTime = dropTime

    def waitStop(self):
        while self.com.isMoving():
            time.sleep(1/self.maxLoop)

    def turnAbsolute(self, movement, angAbsolute):
        reached = False
        finishTime = None
        scale = self.unitRotation/(2.1*math.pi)
        while True:
            x, y, ang = self.com.getPosition()
            change = angAbsolute - ang
            if abs(change) < 0.017:
                if not reached:
                    finishTime = time.time() + 0.5
                    reached = True
                elif time.time() >= finishTime:
                    break

            goal = change*scale

            if movement is not Movement.Spin:
                goal *= 2

            self.com.startMovement(movement, int(goal))

            time.sleep(0.25)

    def turnToBearing(self, movement, direction, bearing):
        x, y, ang = self.com.getPosition()
        if direction:
            while bearing > ang:
                bearing -= 2*math.pi
            while bearing < ang:
                bearing += 2*math.pi
        else:
            while bearing < ang:
                bearing += 2*math.pi
            while bearing > ang:
                bearing -= 2*math.pi

        self.turnAbsolute(movement, bearing)

    def turnToBearingNearest(self, movement, bearing):
        x, y, ang = self.com.getPosition()

        while bearing < ang - math.pi:
            bearing += 2*math.pi
        while bearing >= ang + math.pi:
            bearing -= 2*math.pi

        self.turnAbsolute(movement, bearing)

        # self.turnToBearing(movement, offset > 0, bearing)

    def turnToPosition(self, movement, direction, x, y):
        robX, robY, ang = self.com.getPosition()

        dX = self.unitLength*x - robX
        dY = self.unitLength*y - robY

        self.turnToBearing(movement, direction, math.atan2(dY, dX))
    
    def turnToPositionNearest(self, movement, x, y):
        robX, robY, ang = self.com.getPosition()

        dX = self.unitLength*x - robX
        dY = self.unitLength*y - robY

        self.turnToBearingNearest(movement, math.atan2(dY, dX))

    def moveToPosition(self, x, y, dir):
        self.com.setParameters(0.7, 0.0075)
        robX, robY, ang = self.com.getPosition()
        dist = math.sqrt(pow(robX-x*self.unitLength, 2) + pow(robY-self.unitLength*y, 2))
        if not dir:
            dist = -dist;
        
        self.com.startMovement(Movement.Line, int(dist))
        self.waitStop()

    def turnToStack(self, movement, index):
        x = self.map.stacks[index][0]
        y = self.map.stacks[index][1]

        self.com.setParameters(0.6, 0.0075)
        self.turnToPositionNearest(movement, x, y)

    def moveUptoStack(self, index):
        self.com.setParameters(0.7, 0.0075)
        x = self.map.stacks[index][0]
        y = self.map.stacks[index][1]

        robX, robY, ang = self.com.getPosition()
        dist = math.sqrt(pow(robX-x*self.unitLength, 2) + pow(robY-y*self.unitLength, 2))
        
        self.com.startMovement(Movement.Line, max(0, int(dist-600)))
        self.waitStop()

    def alignCamera(self):
        self.com.setParameters(0.3, 0.0075)
        time.sleep(0.5)
        if self.vis.getPercent(not self.map.primaryRed) < 2.4:
            self.com.startMovement(Movement.Spin, -int(self.unitRotation/8))
            self.waitStop()
        if self.vis.getPercent(not self.map.primaryRed) < 2.4:
            self.com.startMovement(Movement.Spin, int(self.unitRotation/4))
            self.waitStop()
        while True:
            median_x = self.vis.getMedianX(not self.map.primaryRed)

            scale = 0.45

            if abs(median_x) < 8:
                self.com.stopMovement()
                break

            self.com.startMovement(Movement.Spin, int(median_x*scale))

            time.sleep(0.25)

    def grabStack(self, index):
        self.com.motorMove(SmallMotor.Gate, 0, 100)
        time.sleep(1.5)
        self.com.motorMove(SmallMotor.Gate, 0, 0)
        self.com.setParameters(0.25, 0.0075)
        angle = 0
        self.com.moveServo(Servo.Camera, 0)
        self.com.startMovement(Movement.Line, 1300)
        while True:
            if not self.com.isMoving():
                break

            per = self.vis.getPercent(not self.map.primaryRed)
            thresh = 24
            if self.map.primaryRed:
                thresh = 26

            if per >= thresh:
                angle = self.vis.getAngle()
                self.com.setParameters(0.2, 0.0006)
                self.com.startMovement(Movement.Line, 232)
                break

            time.sleep(1/self.maxLoop)
        
        self.waitStop()
        x, y, ang = self.com.getPosition()
        fixedX = self.map.stacks[index][0]*self.unitLength
        fixedY = self.map.stacks[index][1]*self.unitLength
        self.com.setPosition(fixedX, fixedY, ang)

        if abs(angle) > math.pi/5:
            self.com.startMovement(Movement.Spin, 200)
            self.waitStop()
        
        self.com.setParameters(0.4, 0.00075)
        self.com.moveServo(Servo.Camera, 275)
        self.com.motorMove(SmallMotor.Gate, 100, 0)
        time.sleep(2)
        # self.com.startMovement(Movement.Line, -60)
        # self.waitStop()
        # self.com.motorMove(SmallMotor.Gate, 0, 100)
        # time.sleep(1)
        # self.com.startMovement(Movement.Line, -50)
        # self.waitStop()
        # self.com.startMovement(Movement.Spin, int(self.unitRotation/12))
        # self.waitStop()
        # self.com.motorMove(SmallMotor.Gate, 100, 0)
        # time.sleep(2)
        self.com.motorMove(SmallMotor.Gate, 0, 100)
        time.sleep(0.7)
        self.com.motorMove(SmallMotor.Gate, 100, 0)
        time.sleep(2)
        self.com.motorMove(SmallMotor.Gate, 0, 0)

    def sortStack(self):
        self.com.setParameters(0.8, 0.00075)
        self.com.setMotorEnable(LargeMotor.Lift, 1)
        x, y, ang = self.com.getPosition()
        primary = False
        for i in range(3):
            self.com.setMotorDirection(LargeMotor.Lift, 0)
            self.com.setMotorSpeed(LargeMotor.Lift, 40)
            self.com.moveServo(Servo.Gate, 90)

            #TURN
            ##############
            self.com.startMovement(Movement.Line, 200)
            time.sleep(0.6)

            movement = None
            if primary:
                ang += math.pi/2
                movement = Movement.ArcRight
            else:
                ang -= math.pi/2
                movement = Movement.ArcLeft

            self.com.moveServo(Servo.Gate, 310)
            self.turnAbsolute(movement, ang)
            ##############
            primary = not primary

            self.com.setMotorSpeed(LargeMotor.Lift, 35)
            self.com.setMotorDirection(LargeMotor.Lift, 1)
            time.sleep(0.75)
            self.com.startMovement(Movement.Line, 75)
            time.sleep(0.6)
            self.com.setMotorSpeed(LargeMotor.Lift, 40)
            self.com.setMotorDirection(LargeMotor.Lift, 0)
            self.waitStop()
            time.sleep(0.6)

        self.com.setMotorSpeed(LargeMotor.Lift, 0)
        self.com.setMotorEnable(LargeMotor.Lift, 0)
        self.com.setParameters(0.6, 0.00075)

    def dropGround(self):
        self.com.setMotorEnable(LargeMotor.Lift, 0)
        time.sleep(1)
        self.com.moveServo(Servo.LeftChute, 550)
        self.com.setParameters(0.2, 0.00075)
        time.sleep(1)
        self.com.startMovement(Movement.Line, 600)
        self.waitStop()

        self.com.moveServo(Servo.LeftChute, 50)
        self.com.setParameters(0.7, 0.00075)
        time.sleep(0.5)

    def waitDrop(self):
        while time.time() - self.startTime < self.dropTime:
            time.sleep(0.1)

    def dropPlatform(self):
        self.com.moveServo(Servo.LeftChute, 45)
        self.com.moveServo(Servo.RightChute, 530)
        self.com.startMovement(Movement.Line, 100)
        self.waitStop()

        self.com.setMotorEnable(LargeMotor.Lift, 1)
        self.com.setMotorDirection(LargeMotor.Lift, 0)
        self.com.setMotorSpeed(LargeMotor.Lift, 75)
        time.sleep(1)
        self.com.setMotorSpeed(LargeMotor.Chute, 100)
        time.sleep(6.6)
        self.com.setMotorSpeed(LargeMotor.Chute, 0)
        self.com.startMovement(Movement.Line, -450)
        self.waitStop()
        self.com.setParameters(0.3, 0.00075)
        self.com.setMotorCurrent(LargeMotor.Left, 22)
        self.com.setMotorCurrent(LargeMotor.Right, 22)
        self.com.startMovement(Movement.Line, -850)
        self.waitStop()

        self.com.setMotorCurrent(LargeMotor.Chute, 11)
        self.com.setMotorDirection(LargeMotor.Chute, 0)
        self.com.setMotorSpeed(LargeMotor.Chute, 17)
        time.sleep(4)
        self.com.setMotorSpeed(LargeMotor.Chute, 0)
        self.com.setMotorSpeed(LargeMotor.Lift, 25)
        self.com.setMotorDirection(LargeMotor.Lift, 1)
        time.sleep(0.8)
        self.com.setMotorEnable(LargeMotor.Lift, 0)
        self.com.setMotorSpeed(LargeMotor.Lift, 0)
        self.com.moveServo(Servo.RightChute, 0)
        self.com.moveServo(Servo.LeftChute, 550)
        self.com.stopMovement()
        self.com.resetPID()
        time.sleep(0.1)
        self.com.setMotorCurrent(LargeMotor.Left, 80)
        self.com.setMotorCurrent(LargeMotor.Right, 80)
        time.sleep(1)
        self.com.startMovement(Movement.Line, 600)
        self.com.setMotorCurrent(LargeMotor.Chute, 100)
        time.sleep(0.2)
        self.com.setMotorDirection(LargeMotor.Chute, 1)
        self.com.setMotorSpeed(LargeMotor.Chute, 80)
        time.sleep(1)
        self.com.setMotorSpeed(LargeMotor.Chute, 0)
        self.com.setMotorDirection(LargeMotor.Chute, 0)
        self.waitStop()

        self.com.moveServo(Servo.RightChute, 520)
        self.com.moveServo(Servo.LeftChute, 50)

        self.com.setMotorSpeed(LargeMotor.Chute, 100)
        while not self.com.getSwitch(Switch.ChuteLimit):
            time.sleep(1/self.maxLoop)
        self.com.setMotorSpeed(LargeMotor.Chute, 0)