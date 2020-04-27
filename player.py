import pygame
import random

pygame.init()

def getTile(x, y, level):
    levelwidth = len(level[0])
    levelheight = len(level)
    if(x < levelwidth and y < levelheight and x >= 0 and y >= 0):
        return level[int(y)][int(x)]

    else:
        return 0

class Player():
    def __init__(self, pspeed, level, screenwidth, screenheight, tilewidth, tileheight, gun1, gun2):
        self.x = random.randint(0, len(level[0]) - 1)
        self.y = random.randint(0, len(level) - 1)
        while(level[self.y][self.x] != 0):
            self.x = random.randint(0, len(level[0]) - 1)
            self.y = random.randint(0, len(level) - 1)

        self.pspeed = pspeed
        self.toggle = 1
        self.level = level
        self.levelwidth = len(level[0])
        self.levelheight = len(level)
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.tilewidth = tilewidth
        self.tileheight = tileheight
        self.cameraposx = 0
        self.cameraposy = 0
        self.guntoggle = 0
        self.gun1 = gun1
        self.gun2 = gun2
        self.gun = gun1

    def shoot(self, win):
        self.gun.shoot(win, self.x, self.y, self.cameraposx, self.cameraposy, self.level, self.tilewidth, self.tileheight)
        self.gun1.updateBullets(win, self.tilewidth, self.tileheight, self.cameraposx, self.cameraposy)
        self.gun2.updateBullets(win, self.tilewidth, self.tileheight, self.cameraposx, self.cameraposy)

    def drawPlayer(self, win, cameraposx, cameraposy):
        pygame.draw.rect(win, (0, 255, 0), (self.x * self.tilewidth - cameraposx * self.tilewidth, self.y * self.tileheight - cameraposy * self.tileheight, self.tilewidth, self.tileheight))

    def setCamera(self, cameraoffsetx, cameraoffsety):
        cameraposx = self.x - cameraoffsetx
        cameraposy = self.y - cameraoffsety

        if(cameraposx <= 0):
            cameraposx = 0

        if(cameraposy <= 0):
            cameraposy = 0

        camerarangex = int(self.screenwidth / self.tilewidth) + cameraposx
        camerarangey = int(self.screenheight / self.tileheight) + cameraposy

        if(camerarangey  >= self.levelheight):
            cameraposy = self.levelheight - (cameraoffsety * 2) - 1

        if(camerarangex >= self.levelwidth):
            cameraposx = self.levelwidth - (cameraoffsetx * 2) - 1

        self.cameraposx = cameraposx
        self.cameraposy = cameraposy

        return cameraposx, cameraposy

    def update(self):
        keys = pygame.key.get_pressed()

        playervely = 0
        playervelx = 0

        if(keys[pygame.K_w]):
            playervely = -self.pspeed

        if(keys[pygame.K_s]):
            playervely = self.pspeed

        if(keys[pygame.K_a]):
            playervelx = -self.pspeed

        if(keys[pygame.K_d]):
            playervelx = self.pspeed

        newplayerx = self.x + playervelx
        newplayery = self.y + playervely

        if(playervelx <= 0):
            if(getTile(newplayerx + 0, self.y + 0, self.level) != 0 or getTile(newplayerx + 0, self.y + 0.9, self.level) != 0):
               newplayerx = int(newplayerx + 1)
               playervelx = 0

        else:
            if(getTile(newplayerx + 1, self.y + 0, self.level) != 0 or getTile(newplayerx + 1, self.y + 0.9, self.level) != 0):
               newplayerx = int(newplayerx)
               playervelx = 0

        if(playervely <= 0):
            if(getTile(newplayerx + 0, newplayery + 0, self.level) != 0 or getTile(newplayerx + 0.9, newplayery + 0, self.level) != 0):
               newplayery = int(newplayery + 1)
               playervely = 0

        else:
            if(getTile(newplayerx + 0, newplayery + 1, self.level) != 0 or getTile(newplayerx + 0.9, newplayery + 1, self.level) != 0):
               newplayery = int(newplayery)
               playervely = 0
               onground = True

            else:
                onground = False

        self.x = newplayerx
        self.y = newplayery

        if(self.x <= 0):
            self.x = 0

        if(self.y <= 0):
            self.y = 0

        if(self.x + 1 >= self.levelwidth):
            self.x = self.levelwidth - 1

        if(self.y + 1 >= self.levelheight):
            self.y = self.levelheight - 1

        if(keys[pygame.K_q]):
            if(self.toggle == 1):
                self.guntoggle = self.guntoggle + 1
                self.gun.reload = False
                if(self.guntoggle % 2 == 0):
                    self.gun = self.gun1

                else:
                    self.gun = self.gun2

            self.toggle = 0

        else:
            self.toggle = 1

        return self.x, self.y
