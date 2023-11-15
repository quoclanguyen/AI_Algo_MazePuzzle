import pygame
from MazeGrid import MazeGrid
from MazeAI import find_path_with_key
from colors import colors

colorsData = colors()

class MazeGUI:
    def __init__(self, width, height, margin, size, caption):
        self.grid = MazeGrid(size)
        self.width = width
        self.height = height
        self.margin = margin
        self.caption = caption
        self.done = False
        self.clock = pygame.time.Clock()
    def createMainWindow(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
        self.font = pygame.font.Font('font\Comfortaa-Regular.ttf', self.margin * 7)
    
    def clear_path(self):
        if self.grid.hasGoalPath():
            self.grid.setBackPath()
        self.drawGrid()

    def go(self, algo):
        self.clear_path()
        if (self.grid.hasStartPoint() and self.grid.hasGoalPoint()):
            find_path_with_key(self, self.grid, algo)

    def handleKeyPress(self, key):
        if key == pygame.K_ESCAPE:
            pygame.quit()
        if key == pygame.K_s:
            self.grid.save('.\maze\savedMaze.txt')
        if key == pygame.K_l:
            self.grid.load('.\maze\defaultMaze.txt')
        if key == pygame.K_f:
            self.grid.fillWall()
        if key == pygame.K_r:
            self.grid.fillPath()
        if key == pygame.K_u:
            self.go("UCS")
        if key == pygame.K_RETURN:
            self.go("A-star")
        if key == pygame.K_b:
            self.go("BFS")
        if key == pygame.K_d:
            self.go("DFS")
    def mouseInGrid(self, x, y):
        return (x < self.grid.size) and (y < self.grid.size)
    
    def handleLeftMousePress(self, x, y):
        # Check whether the mouse hover in the grid
        if not self.mouseInGrid(x, y):
            return
        # if ()
        if self.grid.hasGoalPath():
            self.grid.setBackPath()
        # Set grid value
        self.grid.set(x, y, self.grid.wall)

    def handleRightMousePress(self, x, y):
        # Check whether the mouse hover in the grid
        if not self.mouseInGrid(x, y):
            return
        
        if self.grid.hasGoalPath():
            self.grid.setBackPath()
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
        if self.grid.hasGoalPath():
            self.grid.setBackPath()
        
        # Check whether the mouse hover in the grid
        if not self.mouseInGrid(x, y):
            return
        
        # Set grid value
        self.grid.set(x, y, self.grid.key)

    def drawGrid(self):
        for row in range(self.grid.size):
            for col in range(self.grid.size):
                colorID = self.grid.get(row, col)
                color = colorsData.gridColors[colorID]
                rect = [
                    self.margin + (self.margin + self.grid.width) * col, 
                    self.margin + (self.margin + self.grid.height) * row, 
                    self.grid.width, 
                    self.grid.height
                ]
                pygame.draw.rect(self.screen, color, rect)
        pygame.display.flip()

    def drawBackground(self):
        self.screen.fill(colorsData.bgColor)

    def setGridSize(self, gwidth, gheight):
        self.grid.width, self.grid.height = gwidth, gheight

    def drawButtons(self):
        btnAstar = [
            round(self.width*0.65),
            round(self.height*0.1),
            self.grid.width * 5, 
            self.grid.height * 3
        ]
        pygame.draw.rect(self.screen, colorsData.gridColors[self.grid.gpath], btnAstar)
        self.screen.blit(
            self.font.render('A-star', True, colorsData.textFG, colorsData.textBG), 
            btnAstar)
        pygame.display.flip()

    def mainLoop(self):
        self.createMainWindow()
        self.drawBackground()
        LEFT_MOUSE = 0
        MID_MOUSE = 1
        RIGHT_MOUSE = 2

        while not self.done:
            mousePos = pygame.mouse.get_pos()
            row = mousePos[0] // (self.grid.height + self.margin)
            col = mousePos[1] // (self.grid.width + self.margin)
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
            # self.drawButtons()
            self.drawGrid()
            self.clock.tick(60)
        
        pygame.quit()

    