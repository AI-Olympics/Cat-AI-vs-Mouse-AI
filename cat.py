#Cat class -- as of now loads images and draws them on the surface
import pygame
import random

RED = (230, 0, 0)


class Cat():

    def __init__(self, gameDisplay, width, height):
        self.DISPLAY = gameDisplay
        self.WIDTH = width 
        self.HEIGHT = height
        
        self.IMG = pygame.image.load('pics/cat2.png')
        self.IMG = pygame.transform.scale(self.IMG, (self.WIDTH, self.HEIGHT))


    def draw(self, x, y):
        self.DISPLAY.blit(self.IMG, (x*self.WIDTH, y*self.HEIGHT))
    