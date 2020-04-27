import pygame

import BSP
import colours

def game(width, height, fullscreen):
    pygame.init()

    win = pygame.display.set_mode((width, height))

    dg = BSP.Generator(100, 100)
    dg.generatemap()
    level = dg.returnmap()

    clock = pygame.time.Clock()

    run = True
    while(run):
        clock.tick(30)
        win.fill(colours.BLACK)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()

        pygame.display.update()
