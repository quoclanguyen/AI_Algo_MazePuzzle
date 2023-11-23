import pygame
from colors import colors
from PygameComponents import Button, Slider, Dragger
from MazeApp import MazeApp
from tkinter import messagebox, Tk
colorsData = colors()

class HomeGUI:
    def __init__(self, width, height, caption):
        self.size = 10
        self.width = width
        self.height = height
        self.caption = caption
        self.margin = 3
        self.resize = False
        self.done = False
        self.ai = False
        self.human = False
        self.clock = pygame.time.Clock()
        self.levels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120]
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
        self.font = pygame.font.Font('font\Minecraft.ttf', 20)
        infos = [
            "AI Project - Group 5:",
            "21110837 - Nguyen Quoc Lan",
            "21110822 - Vo Minh Dat",
            "21110154 - Tran Dinh Duy",
            "Solving maze game using AI search algorithms"
        ]
        for i in range(len(infos)):
            if i == len(infos) - 1:
                self.font = pygame.font.Font('font\Minecraft.ttf', 30)
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
        if self.ai == False and self.human == False:
            tempTk = Tk()
            tempTk.withdraw()
            messagebox.showwarning(
                "Notification",
                "You must choose a game mode"
            )
            tempTk.destroy()
            return
        mode = "ai" if self.ai else "human"
        MazeApp(self.size, self.width, self.height, mode)
        self.drawBackground()
    def exitButton(self):
        self.done = True
    def sliderHandler(self, mousePos):
        self.dragger.rectx = mousePos[0]
        self.drawSlider()
    def drawDragger(self):
        # 11 level of size: 10, 20, 30, 40, 50
        # 60
        # 70, 80, 90, 100, 120
        level = {}
        count = -5
        for item in self.levels:
            level[item] = count
            count += 1
        self.dragger = Dragger(
            (self.width - (63 - level[self.size]*108)/2)//2,
            (self.slider.rect[1] - 9),
            "./images/Dragger.png",
            0.5
        )
        self.dragger.draw(self.screen)
        pygame.time.delay(60)
    def drawSlider(self):
        self.slider = Slider(
            (self.width - 657/2)//2,
            self.buttons["Size"].rect[1] + 100,
            "./images/Slider.png",
            0.5
        )
        self.slider.draw(self.screen)
    def aiButton(self):
        self.human = False
        self.ai = True
    def humanButton(self):
        self.human = True
        self.ai = False
    def sizeButton(self):
        self.resize = True
    def okButton(self):
        self.resize = False
        self.clearSlider()
    def prevButton(self):
        index = self.levels.index(self.size)
        if index > 0:
            self.size = self.levels[index - 1]
    def nextButton(self):
        index = self.levels.index(self.size)
        if index < len(self.levels) - 1:
            self.size = self.levels[index + 1]
    def drawing(self):
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
        
        ai_disabled = "./images/AI_disabled.png"
        human_disabled = "./images/Human_disabled.png"
        ai_enabled = "./images/AI.png"
        human_enabled = "./images/Human.png"
        aiSrc = ai_enabled
        humanSrc = human_enabled

        if self.ai == True:
            aiSrc = ai_enabled
            humanSrc = human_disabled
        if self.human == True:
            aiSrc = ai_disabled
            humanSrc = human_enabled
            
        self.buttons["AI"] = Button(
            (self.width + 279/2)//2, 
            self.height - 200,
            aiSrc,
            0.5
        )
        self.buttons["Human"] = Button(
            (self.width + 279/2)//2 - 279, 
            self.height - 200,
            humanSrc,
            0.5
        )

        self.buttons["Start"].draw(self.screen, self.startButton)
        self.buttons["Exit"].draw(self.screen, self.exitButton)
        self.buttons["Size"].draw(self.screen, self.sizeButton)
        self.buttons["Human"].draw(self.screen, self.humanButton)
        self.buttons["AI"].draw(self.screen, self.aiButton)
        self.font = pygame.font.Font('font\Minecraft.ttf', 25)
        currentSize = self.font.render("Current size: " + str(self.size), True, colorsData.darkerPath)
        
        pygame.display.flip()
        if self.resize == False:
            self.clearSlider()
            return
        self.clearSlider()
        self.drawSlider()
        self.drawDragger()
        self.screen.blit(
            currentSize, 
            (self.slider.rect.left - 250, 
            self.slider.rect.y)
        )
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
            self.drawing()
            self.clock.tick(60)
        pygame.quit()

    