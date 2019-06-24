#mouse class - as of now loads images and draws them on the surface

#cat class
import pygame
import random
from Agent import Q_Agent

GREEN = (0,230,0)

class Mouse(Q_Agent):

    def __init__(self, gameDisplay, width, height):
        self.DISPLAY = gameDisplay
        self.WIDTH = width 
        self.HEIGHT = height
    
        self.IMG = pygame.image.load('pics/mouse4.png')
        self.IMG = pygame.transform.scale(self.IMG, (self.WIDTH, self.HEIGHT))

    def draw(self, x, y):
        self.DISPLAY.blit(self.IMG, (x*self.WIDTH, y*self.HEIGHT))
        #pygame.draw.rect(self.DISPLAY, GREEN, [x*self.WIDTH, y*self.HEIGHT, self.WIDTH, self.HEIGHT])

        