import numpy

class MazeGrid:
    def __init__(self):
        self.data = [[0 for x in range(33)] for y in range(33)]
        self.weight = 0
        self.height = 0
        self.path = 0
        self.wall = 1
        self.start = 2
        self.goal = 3
        self.gpath = 4
        self.key = 5
    def get(self, x, y):
        return int(self.data[x][y])
    def set(self, x, y, value):
        self.data[x][y] = value
    def save(self, filename):
        numpy.savetxt(filename, numpy.array(self.data), fmt="%i")
    def load(self, filename):
        self.data = numpy.loadtxt(filename).tolist()
    def hasStartPoint(self):
        return sum(x.count(self.start) for x in self.data) >= 1
    def hasGoalPoint(self):
        return sum(x.count(self.goal) for x in self.data) >= 1
    def fillWall(self):
        for x in range(33):
            for y in range(33):
                self.data = self.set(x, y, self.wall)
    def fillPath(self):
        for x in range(33):
            for y in range(33):
                self.data = self.set(x, y, self.path)