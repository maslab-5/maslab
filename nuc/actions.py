from command import Movement, Servo, SmallMotor, LargeMotor, Switch

import math
import time

class Actions:
    def __init__(self, map, command, visual, unitLength, unitRotation, maxLoop):
        self.map = map
        self.com = command
        self.vis = visual

        self.unitLength = unitLength
        self.unitRotation = unitRotation

        self.maxLoop = maxLoop

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

        scale = self.unitRotation/(2.3*math.pi)
        reached = False
        finishTime = None
        while True:
            x, y, ang = self.com.getPosition()
            change = bearing - ang
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

    def turnToBearingNearest(self, movement, bearing):
        x, y, ang = self.com.getPosition()
        offset = bearing - ang

        while offset >= math.pi:
            offset -= 2*math.pi
        while offset < -math.pi:
            offset += 2*math.pi

        self.turnToBearing(movement, offset > 0, bearing)

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
        robX, robY, ang = self.com.getPosition()
        dist = math.sqrt(pow(robX-x*self.unitLength, 2) + pow(robY-self.unitLength*y, 2))
        if not dir:
            dist = -dist;
        
        self.com.startMovement(Movement.Line, int(dist))

        while self.com.isMoving():
            time.sleep(1/self.maxLoop)

    def turnToStack(self, movement, index):
        x = self.map.stacks[index][0]
        y = self.map.stacks[index][1]

        self.turnToPositionNearest(movement, x, y)

    def moveUptoStack(self, index):
        approach = 600

        x = self.map.stacks[index][0]
        y = self.map.stacks[index][1]

        robX, robY, ang = self.com.getPosition()
        dist = math.sqrt(pow(robX-x*self.unitLength, 2) + pow(robY-y*self.unitLength, 2))
        
        self.com.startMovement(Movement.Line, max(0, int(dist-approach)))
        
        while self.com.isMoving():
            time.sleep(1/self.maxLoop)

    def alignCamera(self):
        while True:
            median_x = self.vis.getMedianX(not self.map.primaryRed)

            scale = 0.3

            if abs(median_x) < 5:
                self.com.stopMovement()
                break

            self.com.startMovement(Movement.Spin, int(median_x*scale))

            time.sleep(0.25)
        

    def grabStack(self):
        angle = 0
        self.com.moveServo(Servo.Camera, 0)
        self.com.startMovement(Movement.Line, 1500)
        while True:
            if not self.com.isMoving():
                break

            per = self.vis.getPercent(not self.map.primaryRed)

            if per >= 30:
                angle = self.vis.getAngle()
                self.com.setParameters(0.1, 0.0006)
                self.com.startMovement(Movement.Line, 275)
                break

            time.sleep(1/self.maxLoop)
        
        while self.com.isMoving():
            time.sleep(1/self.maxLoop)

        if abs(angle) > math.pi/5:
            self.com.startMovement(Movement.Spin, 200)
            while self.com.isMoving():
                time.sleep(1/self.maxLoop)
        
        self.com.motorMove(SmallMotor.GateMotor, 100, 0)
        self.com.setParameters(0.4, 0.00075)
        self.com.moveServo(Servo.Camera, 250)
        time.sleep(1.5)
        self.com.motorMove(SmallMotor.GateMotor, 0, 0)

    def sortStack(self):
        self.com.setParameters(1, 0.001)
        primary = not self.map.primaryRed
        for i in range(3):
            self.com.motorMove(SmallMotor.LiftMotor, 0, 90)#move picker up
            x, y, ang = self.com.getPosition()
            self.com.moveServo(Servo.Gate, 0)
            self.com.startMovement(Movement.Line, 120)

            time.sleep(0.2)

            if primary:
                self.com.startMovement(Movement.PivotRight, self.unitRotation*2)
            else:
                self.com.startMovement(Movement.PivotLeft, -self.unitRotation*2)
            
            time.sleep(0.85)
            self.com.moveServo(Servo.Gate, 400)

            while self.com.isMoving():
                time.sleep(1/self.maxLoop)
            primary = not primary

            self.com.motorMove(SmallMotor.LiftMotor, 90, 0)#move picker down
            time.sleep(1.5)

        self.com.setParameters(0.4, 0.00075)
        self.com.motorMove(SmallMotor.LiftMotor, 0, 0)

    def dropGround(self):
        self.com.moveServo(Servo.LeftChute, 550)
        self.com.setParameters(0.2, 0.00075)
        time.sleep(1)
        self.com.startMovement(Movement.Line, 650)
        while self.com.isMoving():
                time.sleep(1/self.maxLoop)
        self.com.moveServo(Servo.LeftChute, 50)

    def waitUntil(self, time):
        ...

    def moveToPlatform(self):
        ...

    def dropPlatform(self):
        self.com.setMotorSpeed(LargeMotor.Chute, 100)
        time.sleep(6.2)
        self.com.setMotorSpeed(LargeMotor.Chute, 0)
        self.com.setParameters(0.15, 0.0005)
        self.com.setMotorCurrent(LargeMotor.Left, 17)
        self.com.setMotorCurrent(LargeMotor.Right, 17)
        self.com.startMovement(Movement.Line, -800)
        while self.com.isMoving():
                time.sleep(1/self.maxLoop)
        time.sleep(1.5)
        self.com.setMotorCurrent(LargeMotor.Chute, 10)
        self.com.setMotorDirection(LargeMotor.Chute, 0)
        self.com.setMotorSpeed(LargeMotor.Chute, 15)
        time.sleep(3)
        self.com.setMotorSpeed(LargeMotor.Chute, 0)
        time.sleep(0.5)
        self.com.moveServo(Servo.RightChute, 0)
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
        self.com.setMotorCurrent(LargeMotor.Chute, 100)
        self.com.setMotorSpeed(LargeMotor.Chute, 40)
        time.sleep(1)
        self.com.setMotorSpeed(LargeMotor.Chute, 0)
        self.com.setMotorDirection(LargeMotor.Chute, 0)
        while self.com.isMoving():
                time.sleep(1/self.maxLoop)
        self.com.moveServo(Servo.RightChute, 520)

        self.com.setMotorSpeed(LargeMotor.Chute, 100)
        while not self.com.getSwitch(Switch.ChuteLimit):
            time.sleep(1/self.maxLoop)
        self.com.setMotorSpeed(LargeMotor.Chute, 0)