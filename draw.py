import pygame

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

class Render():
    def __init__(self, level, tilewidth, tileheight):
        self.level = level
        self.tilewidth = tilewidth
        self.tileheight = tileheight

    def initImages(self):
        self.sand = pygame.image.load("sand.png")

    def drawLevel(self, cameraposx, cameraposy, camerarangex, camerarangey, player, win):
        for x in range(len(self.level[0])):
            for y in range(len(self.level)):
                if(x - 1 <= cameraposx + camerarangex and x >= cameraposx - 1 and y - 1 <= cameraposy + camerarangey and y >= cameraposy - 1):
                    tile = self.level[y][x]
                    if(tile == 0):
                        pygame.draw.rect(win, BLUE, (x * self.tilewidth - cameraposx * self.tilewidth, y * self.tileheight - cameraposy * self.tileheight, self.tilewidth, self.tileheight))
                        #win.blit(self.sand, (x * self.tilewidth - cameraposx * self.tilewidth, y * self.tileheight - cameraposy * self.tileheight))

                    elif(tile == 1):
                        pygame.draw.rect(win, BROWN, (x * self.tilewidth - cameraposx * self.tilewidth, y * self.tileheight - cameraposy * self.tileheight, self.tilewidth, self.tileheight))

                    elif(tile == 2):
                        pygame.draw.rect(win, RED, (x * self.tilewidth - cameraposx * self.tilewidth, y * self.tileheight - cameraposy * self.tileheight, self.tilewidth, self.tileheight))

                    elif(tile == 3):
                        pygame.draw.rect(win, CYAN, (x * self.tilewidth - cameraposx * self.tilewidth, y * self.tileheight - cameraposy * self.tileheight, self.tilewidth, self.tileheight))

                    elif(tile == 4):
                        pygame.draw.rect(win, YELLOW, (x * self.tilewidth - cameraposx * self.tilewidth, y * self.tileheight - cameraposy * self.tileheight, self.tilewidth, self.tileheight))

                    elif(tile == 5):
                        pygame.draw.rect(win, PURPLE, (x * self.tilewidth - cameraposx * self.tilewidth, y * self.tileheight - cameraposy * self.tileheight, self.tilewidth, self.tileheight))

                    elif(tile == 6):
                        pygame.draw.rect(win, GREY, (x * self.tilewidth - cameraposx * self.tilewidth, y * self.tileheight - cameraposy * self.tileheight, self.tilewidth, self.tileheight))

                    elif(tile == 7):
                        pygame.draw.rect(win, ORANGE, (x * self.tilewidth - cameraposx * self.tilewidth, y * self.tileheight - cameraposy * self.tileheight, self.tilewidth, self.tileheight))

                    else:
                        pygame.draw.rect(win, BLACK, (x * self.tilewidth - cameraposx * self.tilewidth, y * self.tileheight - cameraposy * self.tileheight, self.tilewidth, self.tileheight))

        player.drawPlayer(win, cameraposx, cameraposy)
