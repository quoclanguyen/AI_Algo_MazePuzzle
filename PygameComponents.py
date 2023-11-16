import pygame as pg
class Button:
    def __init__(self, x, y, imgPath, scale):
        self.imgPath = imgPath
        image = pg.image.load(imgPath).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.scale = scale
        self.image = pg.transform.scale(image, (int(self.scale * width), int(self.scale * height)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self, surface, command):
        pos = pg.mouse.get_pos()
        LEFT_MOUSE = 0
        if self.rect.collidepoint(pos):
            pressed = "images/" + self.imgPath.split("/")[-1].split(".")[0] + "_pressed.png"
            self.changeImg(pressed)
            if pg.mouse.get_pressed()[LEFT_MOUSE]:
                command()
        surface.blit(self.image, (self.rect.x, self.rect.y))
    def changeImg(self, c_imgPath):
        image = pg.image.load(c_imgPath).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(self.scale * width), int(self.scale * height)))

class Slider:
    def __init__(self, x, y, imgPath, scale):
        image = pg.image.load(imgPath).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.scale = scale
        self.image = pg.transform.scale(image, (int(self.scale * width), int(self.scale * height)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Dragger:
    def __init__(self, x, y, imgPath, scale):
        self.imgPath = imgPath
        image = pg.image.load(imgPath).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.scale = scale
        self.image = pg.transform.scale(image, (int(self.scale * width), int(self.scale * height)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))