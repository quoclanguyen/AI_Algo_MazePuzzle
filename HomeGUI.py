import pygame
from colors import colors
from PygameComponents import Button, Slider, Dragger
from MazeApp import MazeApp

colorsData = colors()

class HomeGUI:
    def __init__(self, width, height, caption):
        self.size = 20
        self.width = width
        self.height = height
        self.caption = caption
        self.margin = 3
        self.resize = False
        self.done = False
        self.clock = pygame.time.Clock()
    def createMainWindow(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)

    def handleKeyPress(self, key):
        if key == pygame.K_ESCAPE:
            pygame.quit()
    def clearSlider(self):
        sliderRect = [
            0,
            self.margin + 270,
            self.width * 2, 100
        ]
        self.screen.fill(colorsData.bgColor, sliderRect)

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
                3 * self.margin * (3 * i + 1) + 400)
            else:
                info = self.font.render(infos[i], True, colorsData.darkerPath)
                rect = info.get_rect()
                rect.topleft = (
                    (self.width - 279)//2, 
                    3 * self.margin * (3 * i + 1) + 400)
            self.screen.blit(
                info, 
                (rect.x,
                rect.y))
            pygame.display.flip()    
    def startButton(self):
        MazeApp(self.size)
        self.drawBackground()
    def exitButton(self):
        self.done = True
    def sliderHandler(self, mousePos):
        self.dragger.rectx = mousePos[0]
        self.drawSlider()
    def drawDragger(self):
        self.dragger = Dragger(
            (self.width - 63/2)//2,
            (self.slider.rect[1] - 9),
            "./images/Dragger.png",
            0.5
        )
        self.dragger.draw(self.screen)
    def drawSlider(self):
        self.slider = Slider(
            (self.width - 657/2)//2,
            self.buttons["Size"].rect[1] + 100,
            "./images/Slider.png",
            0.5
        )
        self.slider.draw(self.screen)
        self.drawDragger()

    def sizeButton(self):
        self.resize = True
    def okButton(self):
        self.resize = False
        self.clearSlider()
    def prevButton(self):
        return
    def nextButton(self):
        return
    def drawButtons(self):
        btnNames = [
            "./images/Start.png",
            "./images/Exit.png",
            "./images/Size.png"
        ]
        self.buttons = {}
        for i in range(len(btnNames)):
            btn = btnNames[i].split("/")[-1].split(".")[0]
            self.buttons[btn] = Button(
                (self.width - 279/2)//2, 
                self.margin + 100 * i, 
                btnNames[i],
                0.5
            )
        
        self.buttons["Start"].draw(self.screen, self.startButton)
        self.buttons["Exit"].draw(self.screen, self.exitButton)
        self.buttons["Size"].draw(self.screen, self.sizeButton)
        pygame.display.flip()
        if self.resize == False:
            self.clearSlider()
            return
        self.drawSlider()
        self.buttons["OK"] = Button(
            self.slider.rect.right + 70, 
            self.slider.rect.y - 18, 
            "./images/OK.png",
            0.5
        )
        self.buttons["Prev"] = Button(
            self.slider.rect.left - 30, 
            self.slider.rect.y, 
            "./images/Prev.png",
            0.5
        )
        self.buttons["Next"] = Button(
            self.slider.rect.right + 10, 
            self.slider.rect.y, 
            "./images/Next.png",
            0.5
        )
        self.buttons["OK"].draw(self.screen, self.okButton)
        self.buttons["Prev"].draw(self.screen, self.prevButton)
        self.buttons["Next"].draw(self.screen, self.nextButton)

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

    