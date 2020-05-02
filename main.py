import pygame
import ctypes

import BSP
import player
import gun
import draw

user32 = ctypes.windll.user32

owidth, oheight = int(user32.GetSystemMetrics(0) / 2), int(user32.GetSystemMetrics(1) / 2)
width, height = owidth, oheight

visibletilesx = width / 32
visibletilesy = height / 32

pygame.init()
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
win = pygame.display.set_mode((width, height), 16)
pygame.display.set_caption("RogueLike")

cursor = pygame.image.load("cursor.png")
ammoback = pygame.image.load("ammoborder.png")

dg = BSP.Generator(100, 100)
dg.generatemap()
level = dg.returnmap()

levelwidth = len(level[0])
levelheight = len(level)

def getTile(x, y):
    global level
    global levelwidth
    global levelheight
    if(x < levelwidth and y < levelheight and x >= 0 and y >= 0):
        return level[int(y)][int(x)]

    else:
        return 0

tilewidth = int(width / visibletilesx)
tileheight = int(height / visibletilesy)

cameraposx = 0
cameraposy = 0
camerarangex = int(width / tilewidth) + cameraposx
camerarangey = int(height / tileheight) + cameraposy

cameraoffsetx = ((width / 2) / tilewidth) - ((tilewidth/2)/tilewidth)
cameraoffsety = ((height / 2) / tileheight) - ((tileheight/2)/tileheight)

pspeed = 0.35

revolver = gun.Gun()
shotgun = gun.Gun(5, 25, 35, 0.5, 5, 4)

p1 = player.Player(pspeed, level, width, height, tilewidth, tileheight, revolver, shotgun)

hudfont = pygame.font.SysFont('arial', 30)

render = draw.Render(level, tilewidth, tileheight)

render.initImages()

run = True
clock = pygame.time.Clock()
while(run):
    elapsedtime = clock.tick(30)/33
    win.fill(draw.BLACK)

    playerx, playery = p1.update(elapsedtime)
    cameraposx, cameraposy = p1.setCamera(cameraoffsetx, cameraoffsety)

    camerarangex = int(width / tilewidth) + cameraposx
    camerarangey = int(height / tileheight) + cameraposy

    render.drawLevel(cameraposx, cameraposy, camerarangex, camerarangey, p1, win)

    p1.shoot(win, elapsedtime)

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run = False

        if(event.type == pygame.VIDEORESIZE):
            width, height = event.w, event.h
            win = pygame.display.set_mode((width, height), 16)

            widthmod = width / owidth
            heightmod = height / oheight

            tilewidth = int(width / visibletilesx)
            tileheight = int(height / visibletilesy)

            visibletilesx = width / (32 * widthmod)
            visibletilesy = height / (32 * heightmod)

            p1.tilewidth = (32 * widthmod)
            p1.tileheight = (32 * heightmod)

            render = draw.Render(level, tilewidth, tileheight)

    #################HUD###################
    mousepos = pygame.mouse.get_pos()
    win.blit(cursor, (mousepos[0] - 16, mousepos[1] - 16))

    ammoout = "Ammo: " + str(p1.gun.ammo) + "/" + str(p1.gun.maxammo)
    if(p1.gun.reload):
        ammoout = ammoout + "↑"
    ammosurface = hudfont.render(ammoout, False, draw.WHITE)
    win.blit(ammoback, (width - 145, 0))
    win.blit(ammosurface, (width - 137, 3))

    pygame.display.update()

pygame.quit()
