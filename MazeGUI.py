import pygame
import numpy
from PIL import ImageColor

bgColor = ImageColor.getcolor("#FCBF49", "RGB"),
gridColors = [
    ImageColor.getcolor("#EAE2B7", "RGB"),
    ImageColor.getcolor("#003049", "RGB"),
    ImageColor.getcolor("#D62828", "RGB"),
    ImageColor.getcolor("#5DF95D", "RGB"),
    ImageColor.getcolor("#F77F00", "RGB"),
    ImageColor.getcolor("#000000", "RGB")
]

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
    def fillWall(self):
        for x in range(33):
            for y in range(33):
                self.data = self.set(x, y, self.wall)
    def fillPath(self):
        for x in range(33):
            for y in range(33):
                self.data = self.set(x, y, self.path)

class MazeGUI:
    def __init__(self, width, height, margin, caption):
        self.grid = MazeGrid()
        self.width = width
        self.height = height
        self.margin = margin
        self.caption = caption
        self.done = False
    def createMainWindow(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
    def handleKeyPress(self, key):
        if key == pygame.K_ESCAPE:
            pygame.quit()
        if key == pygame.K_s:
            self.grid.save()
        if key == pygame.K_l:
            self.grid.load('defaultMaze.txt')
        if key == pygame.K_f:
            self.grid.fillWall()
        if key == pygame.K_r:
            self.grid.fillPath()
        if key == pygame.K_RETURN:
            #self.grid.solve()
            pass
    def draw(self):
        self.screen.fill(bgColor)
        for row in range(33):
            for col in range(33):
                colorID = self.grid.get(row, col)
                color = gridColors[colorID]
                rect = [
                    self.margin + (self.margin + self.grid.width) * col, 
                    self.margin + (self.margin + self.grid.height) * row, 
                    self.grid.width, 
                    self.grid.height
                ]
                pygame.draw.rect(self.screen, color, rect)
        pygame.display.flip()
    def setGridSize(self, gwidth, gheight):
        self.grid.width, self.grid.height = gwidth, gheight
    def mainLoop(self):
        self.createMainWindow()
        while not self.done:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyPress(event.key)
            self.draw()
            clock = pygame.time.Clock()
            clock.tick(60)
        pygame.quit()

    