
class Map:
    def __init__(self, mapfile):
        self.startX = 0
        self.startY = 0
        self.startAng = 0

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
        #[x, y, [bottom, middle, top]]
        self.stacks = []

        #[[x1, y1], [x2, y2]]
        self.walls = []

        self.maxY = 0
        self.maxX = 0

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
            self.stacks.append([x, y, [0, 0, 0]])

        self.stacks[index][2][height] = isRed

    def readMap(self, mapfile):
        map = open(mapfile, 'r')
        maplines = map.readlines()
        for mapline in maplines:
            params = mapline.split(",")
            if mapline.startswith("#"):
                continue
            if mapline.startswith("W"):
                x1 = float(params[1])
                y1 = float(params[2])
                x2 = float(params[3])
                y2 = float(params[4])
                self.walls.append([[x1, y1], [x2, y2]])
            elif mapline.startswith("C"):
                self.addCube(float(params[1]), float(params[2]), int(params[3]), ("R" in params[4]))
            elif mapline.startswith("P"):
                self.platformStartX = float(params[1])
                self.platformStartY = float(params[2])
                self.platformEndX = float(params[3])
                self.platformEndY = float(params[4])
            elif mapline.startswith("A"):
                self.tagX = float(params[1])
                self.tagY = float(params[2])
                self.primaryRed = ("R" in params[3])
            elif mapline.startswith("B"):
                self.boxX = float(params[1])
                self.boxY = float(params[2])
            elif mapline.startswith("R"):
                self.startX = float(params[1])
                self.startY = float(params[2])
                self.startAng = 90-float(params[3])
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