import pygame
from MazeGrid import MazeGrid
from MazeAI import find_path_with_key
from colors import colors
from PygameComponents import Button

colorsData = colors()

class MazeAIGUI:
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
            self.grid.save('.\maze\{}\savedMaze.txt'.format(self.grid.size))
        if key == pygame.K_l:
            self.grid.load('.\maze\{}\defaultMaze.txt'.format(self.grid.size))
        if key == pygame.K_f:
            self.grid.fillWall()
        if key == pygame.K_r:
            self.grid.fillPath()
    def mouseInGrid(self, x, y):
        return (x < self.grid.size) and (y < self.grid.size)
    
    def handleLeftMousePress(self, x, y):
        # Check whether the mouse hover in the grid
        if not self.mouseInGrid(x, y):
            return
        
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
        playerImg = pygame.image.load("./images/player.png").convert_alpha()
        playerImg = pygame.transform.scale(playerImg, (self.grid.width, self.grid.height))
        goalImg = pygame.image.load("./images/goal.png").convert_alpha()
        goalImg = pygame.transform.scale(goalImg, (self.grid.width, self.grid.height))
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
                if colorID == self.grid.gpath:
                    continue
                if colorID != self.grid.goal and colorID != self.grid.start:
                    pygame.draw.rect(self.screen, color, rect)
                if colorID == self.grid.start:
                    self.screen.blit(playerImg, rect)
                if colorID == self.grid.goal:
                    self.screen.blit(goalImg, rect)
        pygame.display.flip()

    def drawBackground(self):
        self.screen.fill(colorsData.bgColor)

    def setGridSize(self, gwidth, gheight):
        self.grid.width, self.grid.height = gwidth, gheight

    def astarButton(self):
        self.go("Astar")

    def drawButtons(self):
        btnNames = [
            "./images/Astar.png",
            "./images/BFS.png",
            "./images/DFS.png",
            "./images/Greedy.png",
            "./images/UCS.png",
            "./images/ID.png",
            "./images/Beam.png",
            "./images/Exit.png",
        ]
        self.buttons = {}
        for i in range(len(btnNames)):
            algo = btnNames[i].split("/")[-1].split(".")[0]
            self.buttons[algo] = Button(
                self.width - 340/2, 
                self.margin + 100 * i, 
                btnNames[i],
                0.5
            )
        
        self.buttons["Astar"].draw(self.screen, lambda: self.go("Astar"))
        self.buttons["BFS"].draw(self.screen, lambda: self.go("BFS"))
        self.buttons["DFS"].draw(self.screen, lambda: self.go("DFS"))
        self.buttons["Greedy"].draw(self.screen, lambda: self.go("Greedy"))
        self.buttons["UCS"].draw(self.screen, lambda: self.go("UCS"))
        self.buttons["ID"].draw(self.screen, lambda: self.go("ID"))
        self.buttons["Beam"].draw(self.screen, lambda: self.go("Beam"))
        self.buttons["Exit"].draw(self.screen, self.stop)
    def stop(self):
        self.done = True
    def mainLoop(self):
        self.createMainWindow()
        self.drawBackground()
        self.grid.fillPath()
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
            self.drawButtons()
            self.drawGrid()
            self.clock.tick(60)
        self.drawBackground()
        

    