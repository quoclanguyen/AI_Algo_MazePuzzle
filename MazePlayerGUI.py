from tkinter import Tk, messagebox
import pygame
from MazeGrid import MazeGrid
from MazeAI import calcDirection
from colors import colors
from PygameComponents import Button

colorsData = colors()

class MazePlayerGUI:
    def __init__(self, width, height, margin, size, caption):
        self.grid = MazeGrid(size)
        self.width = width
        self.height = height
        self.margin = margin
        self.caption = caption
        self.done = False
        self.clock = pygame.time.Clock()
        self.direct = "up"
        self.edit = True
        self.moves_played = 0

    def createMainWindow(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
        self.font = pygame.font.Font('font\Minecraft.ttf', 15)
    
    def winNotify(self):
        tempTk = Tk()
        tempTk.withdraw()
        messagebox.showinfo(
            "Congratulations!",
            "YOU WON"
        )
        tempTk.destroy()

    def handleKeyPress(self, key):
        if self.edit == True:
            return
        if not self.grid.hasStartPoint():
            return
        if not self.grid.hasGoalPoint():
            return
        keys = self.grid.findKeys()

        start, _ = self.grid.findSGPoint()
        if key == pygame.K_UP:
            if self.grid.get(start[0] - 1, start[1]) == self.grid.goal and len(keys) == 0:
                self.edit = True
            if self.grid.get(start[0] - 1, start[1]) == self.grid.goal and len(keys) != 0:
                return
            if self.grid.get(start[0] - 1, start[1]) != self.grid.wall:
                self.moves_played += 1
                self.grid.set(*start, self.grid.path)
                self.grid.set(start[0] - 1, start[1], self.grid.start)
                self.direct = "up"
                if self.edit == True: 
                    self.winNotify()
                    return
        
        if key == pygame.K_DOWN:
            if self.grid.get(start[0] + 1, start[1]) == self.grid.goal and len(keys) == 0:
                self.edit = True
                self.winNotify()
            if self.grid.get(start[0] + 1, start[1]) == self.grid.goal and len(keys) != 0:
                return
            if self.grid.get(start[0] + 1, start[1]) != self.grid.wall:
                self.moves_played += 1
                self.grid.set(*start, self.grid.path)
                self.grid.set(start[0] + 1, start[1], self.grid.start)
                self.direct = "down"
                if self.edit == True: 
                    self.winNotify()
                    return

        if key == pygame.K_LEFT:
            if self.grid.get(start[0], start[1] - 1) == self.grid.goal and len(keys) == 0:
                self.edit = True
            if self.grid.get(start[0], start[1] - 1) == self.grid.goal and len(keys) != 0:
                return
            if self.grid.get(start[0], start[1] - 1) != self.grid.wall:
                self.moves_played += 1
                self.grid.set(*start, self.grid.path)
                self.grid.set(start[0], start[1] - 1, self.grid.start)
                self.direct = "left"
                if self.edit == True: 
                    self.winNotify()
                    return

        if key == pygame.K_RIGHT:
            if self.grid.get(start[0], start[1] + 1) == self.grid.goal and len(keys) == 0:
                self.edit = True
            if self.grid.get(start[0], start[1] + 1) == self.grid.goal and len(keys) != 0:
                return
            if self.grid.get(start[0], start[1] + 1) != self.grid.wall:
                self.moves_played += 1
                self.grid.set(*start, self.grid.path)
                self.grid.set(start[0], start[1] + 1, self.grid.start)
                self.direct = "right"
                if self.edit == True: 
                    self.winNotify()
                    return
    
    def mouseInGrid(self, x, y):
        return (x < self.grid.size) and (y < self.grid.size)
    
    def handleLeftMousePress(self, x, y):
        # Check whether the mouse hover in the grid
        if not self.mouseInGrid(x, y):
            return
        if self.edit == False:
            return
        # Set grid value
        self.grid.set(x, y, self.grid.wall)

    def handleRightMousePress(self, x, y):
        # Check whether the mouse hover in the grid
        if not self.mouseInGrid(x, y):
            return
        if self.edit == False:
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
        if self.edit == False:
            return
        # Check whether the mouse hover in the grid
        if not self.mouseInGrid(x, y):
            return
        # Set grid value
        self.grid.set(x, y, self.grid.key)

    def drawGrid(self):
        playerImg = pygame.image.load("./images/player_{}.png".format(self.direct)).convert_alpha()
        playerImg = pygame.transform.scale(playerImg, (self.grid.width, self.grid.height))
        goalImg = pygame.image.load("./images/goal.png").convert_alpha()
        goalImg = pygame.transform.scale(goalImg, (self.grid.width, self.grid.height))
        keyImg = pygame.image.load("./images/key.png").convert_alpha()
        keyImg = pygame.transform.scale(keyImg, (self.grid.width, self.grid.height))
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
                if colorID == self.grid.start:
                    self.screen.blit(playerImg, rect)
                    continue
                if colorID == self.grid.goal:
                    self.screen.blit(goalImg, rect)
                    continue
                if colorID == self.grid.key:
                    self.screen.blit(keyImg, rect)
                    continue
                pygame.draw.rect(self.screen, color, rect)
        pygame.display.flip()

    def drawBackground(self):
        self.screen.fill(colorsData.bgColor)

    def setGridSize(self, gwidth, gheight):
        self.grid.width, self.grid.height = gwidth, gheight
    
    def enableEdit(self):
        self.edit = not self.edit
        self.moves_played = 0
        pygame.time.delay(100)

    def drawButtons(self):
        btnNames = [
            "./images/Play.png",
            "./images/Load.png",
            "./images/Clear.png",
            "./images/Save.png",
            "./images/Exit.png",
        ]
        self.buttons = {}
        for i in range(len(btnNames)):
            algo = btnNames[i].split("/")[-1].split(".")[0]
            self.buttons[algo] = Button(
                self.width - 400/2, 
                self.margin + 50 * i, 
                btnNames[i],
                0.37
            )
        if self.edit == True:
            self.buttons["Play"].draw(self.screen, self.enableEdit)
        else:
            self.buttons["Edit"] = Button(
                self.buttons["Play"].rect.x,
                self.buttons["Play"].rect.y,
                "./images/Edit.png",
                0.37
            )
            self.buttons["Edit"].draw(self.screen, self.enableEdit)
        self.buttons["Load"].draw(self.screen, lambda: self.grid.load('.\maze\{}\defaultMaze.txt'.format(self.grid.size)))
        self.buttons["Clear"].draw(self.screen, lambda: self.grid.fillPath())
        self.buttons["Save"].draw(self.screen, lambda: self.grid.save('.\maze\{}\savedMaze.txt'.format(self.grid.size)))
        self.buttons["Exit"].draw(self.screen, self.stop)
        rect = self.buttons["Exit"].rect
        infoX = rect.x - 70
        infoY = rect.y + 100
        rect = [
            infoX,
            infoY,
            1000,
            100
        ]
        pygame.draw.rect(self.screen, colorsData.bgColor, rect)
        infoMove = self.font.render(
            "Moves played: {}".format(self.moves_played),
            True,
            colorsData.darkerPath
        )
        self.screen.blit(
            infoMove, 
            (infoX, infoY))

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
        

    