import pygame
import bullet

class Gun():
    def __init__(self, maxammo=7, reloadtime=30, cocktime=20, speed=0.7, spread=25, bulletspershot=1):
        self.maxammo = maxammo
        self.ammo = maxammo
        self.reloadtime = reloadtime
        self.reloadtimer = 0
        self.cocktime = cocktime
        self.cocktimer = 0
        self.spread = spread
        self.reload = False
        self.bullets = []
        self.speed = speed
        self.bshot = bulletspershot

    def updateBullets(self, win, tilewidth, tileheight, cameraposx, cameraposy):
        delete = []
        for i in range(len(self.bullets)):
            self.bullets[i].updateBullet()
            self.bullets[i].drawBullet(win, tilewidth, tileheight, cameraposx, cameraposy)
            if(self.bullets[i].show == False):
                delete.append(i)

        for i in delete:
            del self.bullets[i]
            for k in range(len(delete)):
                if(delete[k] > i):
                    delete[k] = delete[k] - 1

    def shoot(self, win, playerx, playery, cameraposx, cameraposy, level, tilewidth, tileheight):
        mousepos = pygame.mouse.get_pos()
        mouseclick = pygame.mouse.get_pressed()

        if(mouseclick[0] and self.cocktimer >= self.cocktime and self.ammo > 0):
            for i in range(self.bshot):
                self.bullets.append(bullet.Bullet(self.speed, playerx, playery, mousepos[0], mousepos[1], tilewidth, tileheight, cameraposx, cameraposy, level, self.spread))
            self.cocktimer = 0
            self.reload = False
            self.reloadtimer = 0
            self.ammo = self.ammo - 1

        self.cocktimer = self.cocktimer + 1

        keys = pygame.key.get_pressed()

        if(self.ammo == 0 or keys[pygame.K_r]):
            self.reload = True

        if(self.ammo >= self.maxammo):
            self.reload = False
            self.reloadtimer = 0

        if(self.reload):
            self.reloadtimer = self.reloadtimer + 1
            if(self.reloadtimer == self.reloadtime):
                self.ammo = self.ammo + 1
                self.reloadtimer = 0
