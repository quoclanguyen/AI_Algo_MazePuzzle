import pygame
from MazeGrid import MazeGrid
from PIL import ImageColor
from MazeAI import a_star

bgColor = ImageColor.getcolor("#FCBF49", "RGB"),
gridColors = [
    ImageColor.getcolor("#EAE2B7", "RGB"),
    ImageColor.getcolor("#003049", "RGB"),
    ImageColor.getcolor("#D62828", "RGB"),
    ImageColor.getcolor("#5DF95D", "RGB"),
    ImageColor.getcolor("#F77F00", "RGB"),
    ImageColor.getcolor("#E47676", "RGB")
]

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
            self.grid.save('savedMaze.txt')
        if key == pygame.K_l:
            self.grid.load('defaultMaze.txt')
        if key == pygame.K_f:
            self.grid.fillWall()
        if key == pygame.K_r:
            self.grid.fillPath()
        if key == pygame.K_RETURN:
            a_star(self.grid)

    def mouseInGrid(self, x, y):
        return (x < 33) and (y < 33)
    
    def handleLeftMousePress(self, x, y):
        # Check whether the mouse hover in the grid
        if not self.mouseInGrid(x, y):
            self.grid.generateNeighbors()
            return
        
        # Set grid value
        self.grid.set(x, y, self.grid.wall)

    def handleRightMousePress(self, x, y):
        # Check whether the mouse hover in the grid
        if not self.mouseInGrid(x, y):
            return
        
        # Set grid value
        if self.grid.get(x, y) in [self.grid.start, self.grid.goal]:
            self.grid.set(x, y, self.grid.path)
            return
        if not self.grid.hasStartPoint():
            self.grid.set(x, y, self.grid.start)
            return
        if not self.grid.hasGoalPoint():
            self.grid.set(x, y, self.grid.goal)
            return
        self.grid.set(x, y, self.grid.path)

    def handleMiddleMousePress(self, x, y):
        # Check whether the mouse hover in the grid
        if not self.mouseInGrid(x, y):
            return
        
        # Set grid value
        self.grid.set(x, y, self.grid.key)

    def drawGrid(self):
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

    def drawButtons(self):
        btnBFS = [
            0,
            0,
            40,
            10
        ]
        pygame.draw.rect(self.screen, gridColors[self.grid.gpath], btnBFS)

    def mainLoop(self):
        self.createMainWindow()
        LEFT_MOUSE = 0
        MID_MOUSE = 1
        RIGHT_MOUSE = 2
        while not self.done:
            mousePos = pygame.mouse.get_pos()
            row = mousePos[0] // (self.grid.height + self.margin)
            col = mousePos[1] // (self.grid.width + self.margin)
            # print(mousePos)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyPress(event.key)
                elif pygame.mouse.get_pressed()[LEFT_MOUSE]:
                    self.handleLeftMousePress(col, row)
                elif pygame.mouse.get_pressed()[MID_MOUSE]:
                    self.handleMiddleMousePress(col, row)
                elif pygame.mouse.get_pressed()[RIGHT_MOUSE]:
                    self.handleRightMousePress(col, row)
            self.drawGrid()
            self.drawButtons()
            clock = pygame.time.Clock()
            clock.tick(60)
        pygame.quit()

    