import pygame #gets pygame module for drawing to resizeable window
import colours #defines colours as tuples for easier reference

#creates a rectange that changes size relative to the screensize
#takes many parameters however most are just external constants
#potentially a memory issue in later stages but for now there is no issue
def drawRect(win, colour, x, y, swidth, sheight, width, height, owidth, oheight):
    widthmod = width / owidth    #find modifier to convert given width and height
    heightmod = height / oheight #to relative width and height based on original
                                 #size of window relative to current size

    ax = int(x * widthmod)  #finds relative position of block to be drawn
    ay = int(y * heightmod) #by using modifiers given above

    awidth = int(swidth * widthmod)    #finds the size of the block to be drawn
    aheight = int(sheight * heightmod) #by using the modifiers found above

    #draws the recgtangle with all the edited values
    pygame.draw.rect(win, colour, (ax, ay, awidth + 1, aheight + 1))
