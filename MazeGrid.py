import numpy

class MazeGrid:
    def __init__(self):
        self.data = [[0 for x in range(33)] for y in range(33)]
        self.neighbors = [[] for _ in range(33**2)]
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
        self.data = numpy.loadtxt(filename, dtype=numpy.int8).tolist()
    def hasStartPoint(self):
        return sum(x.count(self.start) for x in self.data) == 1
    def hasGoalPoint(self):
        return sum(x.count(self.goal) for x in self.data) == 1
    def findSGPoint(self):
        start, goal = 0, 0
        for x in range(33):
            for y in range(33):
                if self.get(x, y) == self.start:
                    start = x, y
                if self.get(x, y) == self.goal:
                    goal = x, y
        return start, goal
    def fillWall(self):
        for x in range(33):
            for y in range(33):
                self.set(x, y, self.wall)
    def fillPath(self):
        for x in range(33):
            for y in range(33):
                self.set(x, y, self.path)
    def generateNeighbors(self):
        count = 0
        direct = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        outer_grid = []
        self.neighbors = [[] for _ in range(33**2)]
        for i in range(35):
            if i == 0 or i == 34:
                outer_grid.append([1 for _ in range(35)])
                continue
            outer_grid.append([1] + self.data[i - 1] + [1])
        for i in range(1, 34):
            for j in range(1, 34):
                for k in range(4):
                    if outer_grid[i + direct[k][0]][j + direct[k][1]] != 1:
                        self.neighbors[count].append((i + direct[k][0] - 1, j + direct[k][1] - 1))
                count += 1
        print(outer_grid)
        print(self.neighbors)