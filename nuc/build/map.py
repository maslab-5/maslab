import math

class Map:
    def __init__(self, mapfile, unitLength):
        self.startX = 0
        self.startY = 0
        self.startAng = 0
        self.unitLength = unitLength

        self.boxX = 0
        self.boxY = 0
        self.tagX = 0
        self.tagY = 0
        self.primaryRed = False

        self.platformStartX = 0
        self.platformStartY = 0
        self.platformEndX = 0
        self.platformEndY = 0

        #color isRed
        #[x, y, [bottom, middle, top], collected]
        self.stacks = []

        #[[x1, y1], [x2, y2]]
        self.walls = []

        self.maxY = 0
        self.maxX = 0

        self.collected = 0

        self.readMap(mapfile)
        self.calcSize()
        self.invertY()

    def addCube(self, x, y, height, isRed):
        index = -1
        for i in range(len(self.stacks)):
            stack = self.stacks[i]
            if stack[0] == x and stack[1] == y:
                index = i
        
        if index == -1:
            self.stacks.append([x, y, [0, 0, 0], 0])

        self.stacks[index][2][height] = isRed

    def readMap(self, mapfile):
        map = open(mapfile, 'r')
        maplines = map.readlines()
        for mapline in maplines:
            params = mapline.split(",")
            if mapline.startswith("#"):
                continue
            if mapline.startswith("W"):
                x1 = float(params[1])*self.unitLength
                y1 = float(params[2])*self.unitLength
                x2 = float(params[3])*self.unitLength
                y2 = float(params[4])*self.unitLength
                self.walls.append([[x1, y1], [x2, y2]])
            elif mapline.startswith("C"):
                self.addCube(float(params[1])*self.unitLength, float(params[2])*self.unitLength, int(params[3]), ("R" in params[4]))
            elif mapline.startswith("P"):
                self.platformStartX = float(params[1])*self.unitLength
                self.platformStartY = float(params[2])*self.unitLength
                self.platformEndX = float(params[3])*self.unitLength
                self.platformEndY = float(params[4])*self.unitLength
            elif mapline.startswith("A"):
                self.tagX = float(params[1])*self.unitLength
                self.tagY = float(params[2])*self.unitLength
                self.primaryRed = ("R" in params[3])
            elif mapline.startswith("B"):
                self.boxX = float(params[1])*self.unitLength
                self.boxY = float(params[2])*self.unitLength
            elif mapline.startswith("R"):
                self.startX = float(params[1])*self.unitLength
                self.startY = float(params[2])*self.unitLength
                self.startAng = math.radians(90-float(params[3]))
                if self.startAng < 0:
                    self.startAng += 360

    def calcSize(self):
        for wall in self.walls:
            if wall[0][1] > self.maxY:
                self.maxY = wall[0][1]
        
        for wall in self.walls:
            if wall[0][0] > self.maxX:
                self.maxX = wall[0][0]

    def invertY(self):
        self.startY = self.maxY - self.startY
        self.boxY = self.maxY - self.boxY
        self.tagY = self.maxY - self.tagY
        self.platformStartY = self.maxY - self.platformStartY
        self.platformEndY = self.maxY - self.platformEndY

        for stack in self.stacks:
            stack[1] = self.maxY - stack[1]

        for wall in self.walls:
            wall[0][1] = self.maxY - wall[0][1]
            wall[1][1] = self.maxY - wall[1][1]

    def nearestCube(self, robX, robY):
        if self.collected == 5:
            return

        shortest = self.maxY*self.maxX
        index = 0
        for i in range(len(self.stacks)):
            if self.stacks[i][3] == 1:
                continue
            dist = math.sqrt(pow(self.stacks[i][0]-robX, 2)+pow(self.stacks[i][1]-robY, 2))
            if dist < shortest:
                shortest = dist
                index = i
        self.stacks[index][3] = 1
        self.collected+=1
        return index, shortest
    
    def angleTo(self, robX, robY, bearing, index):
        dX = self.stacks[index][0] - robX
        dY = self.stacks[index][1] - robY

        changeAng = math.atan2(dY, dX) - bearing
        while changeAng < math.pi:
            changeAng += math.pi*2

        while changeAng >= math.pi:
            changeAng -= math.pi*2

        return changeAng

