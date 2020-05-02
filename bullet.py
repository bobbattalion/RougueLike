import pygame
import math
import random

pygame.init()

def getTile(x, y, level):
    levelwidth = len(level[0])
    levelheight = len(level)
    if(x < levelwidth and y < levelheight and x >= 0 and y >= 0):
        return level[int(y)][int(x)]

    else:
        return 0

class Bullet():
    def __init__(self, speed, x, y, targetx, targety, tilewidth, tileheight, cameraposx, cameraposy, level, spread=25):
        self.speed = speed
        self.x = x + 0.5
        self.screenx = self.x * tilewidth - cameraposx * tilewidth
        self.y = y + 0.5
        self.screeny = self.y * tileheight - cameraposy * tileheight
        self.targetx = targetx
        self.targety = targety
        self.spread = spread
        self.magnitude = math.sqrt((self.targetx - self.screenx) ** 2 + (self.targety - self.screeny) ** 2)
        try:
            self.speedx = ((self.targetx - self.screenx) / self.magnitude) * self.speed + (random.randint(-1, 1)/self.spread)
            self.speedy = ((self.targety - self.screeny) / self.magnitude) * self.speed + (random.randint(-1, 1)/self.spread)

        except:
            self.speedx = random.randint(-1, 1) * math.sqrt(2) * self.speed + (random.randint(-1, 1)/self.spread)
            self.speedy = random.randint(-1, 1) * math.sqrt(2) * self.speed + (random.randint(-1, 1)/self.spread)

        self.level = level
        self.frames = 240
        self.show = True

    def updateBullet(self, elapsedtime):
        if(self.show):
            self.x = self.x + (self.speedx * elapsedtime)
            self.y = self.y + (self.speedy * elapsedtime)

            if(getTile(self.x, self.y, self.level) != 0):
                self.show = False

            self.frames = self.frames - 1

            if(self.frames == 0):
                self.show = False

    def drawBullet(self, win, tilewidth, tileheight, cameraposx, cameraposy):
        if(self.show):
            pygame.draw.circle(win, (255, 255, 0), (int(self.x * tilewidth - cameraposx * tilewidth), int(self.y * tileheight - cameraposy * tileheight)), 10)
