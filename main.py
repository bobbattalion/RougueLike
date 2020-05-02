import pygame

import BSP
import player
import gun
import draw

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
BROWN = (150, 75, 0)
BEIGE = (150, 120, 45)

width = 640
height = 480

pygame.init()
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("ROUGUE LIKE I GUESS")


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

visibletilesx = 20
visibletilesy = 15

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
    elapsedtime = clock.tick(60)/33
    win.fill(BLACK)

    playerx, playery = p1.update(elapsedtime)
    cameraposx, cameraposy = p1.setCamera(cameraoffsetx, cameraoffsety)

    camerarangex = int(width / tilewidth) + cameraposx
    camerarangey = int(height / tileheight) + cameraposy

    render.drawLevel(cameraposx, cameraposy, camerarangex, camerarangey, p1, win)

    p1.shoot(win, elapsedtime)

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run = False

    #################HUD###################
    mousepos = pygame.mouse.get_pos()
    win.blit(cursor, (mousepos[0] - 16, mousepos[1] - 16))

    ammoout = "Ammo: " + str(p1.gun.ammo) + "/" + str(p1.gun.maxammo)
    if(p1.gun.reload):
        ammoout = ammoout + "↑"
    ammosurface = hudfont.render(ammoout, False, WHITE)
    win.blit(ammoback, (width - 145, 0))
    win.blit(ammosurface, (width - 140, 3))

    pygame.display.update()

pygame.quit()
