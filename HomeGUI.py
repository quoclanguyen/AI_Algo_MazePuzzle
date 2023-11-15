import pygame
from colors import colors
from PygameComponents import Button
from MazeApp import MazeApp

colorsData = colors()

class HomeGUI:
    def __init__(self, width, height, caption):
        self.width = width
        self.height = height
        self.caption = caption
        self.margin = 3
        self.done = False
        self.clock = pygame.time.Clock()
    def createMainWindow(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)

    def handleKeyPress(self, key):
        if key == pygame.K_ESCAPE:
            pygame.quit()

    def drawBackground(self):
        self.screen.fill(colorsData.bgColor)
        self.font = pygame.font.Font('font\Comfortaa-Regular.ttf', 25)
        infos = [
            "AI Project - Group 5:",
            "21110837 - Nguyễn Quốc Lân",
            "21110822 - Võ Minh Đạt",
            "21110154 - Trần Đình Duy",
            "Solving maze game using AI search algorithms"
        ]
        for i in range(len(infos)):
            if i == len(infos) - 1:
                self.font = pygame.font.Font('font\Comfortaa-Bold.ttf', 30)
                info = self.font.render(infos[i], True, colorsData.gridColors[2])
                rect.topleft = (
                (self.width - 279*2.5)//2, 
                3 * self.margin * (3 * i + 1) + 200)
            else:
                info = self.font.render(infos[i], True, colorsData.darkerPath)
                rect = info.get_rect()
                rect.topleft = (
                    (self.width - 279)//2, 
                    3 * self.margin * (3 * i + 1) + 200)
            self.screen.blit(
                info, 
                (rect.x,
                rect.y))
            pygame.display.flip()    
    def startButton(self):
        MazeApp(12)
    def endButton(self):
        self.done = True
    def drawButtons(self):
        btnNames = [
            "./images/Start.png",
            "./images/Exit.png"
        ]
        self.buttons = []
        for i in range(len(btnNames)):
            self.buttons.append(Button(
                (self.width - 279/2)//2, 
                self.margin + 100 * i, 
                btnNames[i],
                0.5
            ))
        self.buttons[0].draw(self.screen, self.startButton)
        self.buttons[1].draw(self.screen, self.endButton)
        pygame.display.flip()

    def mainLoop(self):
        self.createMainWindow()
        self.drawBackground()

        while not self.done:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyPress(event.key)
            self.drawButtons()
            self.clock.tick(60)
        pygame.quit()

    