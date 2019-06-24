#Environment
import pygame
import numpy as np 
import random
import time
from collections import deque 

from cat import Cat 
from mouse import Mouse

#colours - r,g,b
WHITE = (255,255,255)
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
TEXT_COLOR = (0,0,220)

class Game_Env():

    def __init__(self, gameDisplay, game_matrix):

        self.HEIGHT = game_matrix.ROWS  #height of the environment
        self.WIDTH = game_matrix.COLUMNS   #width of the environment

        self.DISPLAY = gameDisplay   #will be used for rendering
        
        display_width, display_height = gameDisplay.get_size()
        display_height -= 100   #since we need some space to show important data.
        
        self.BLOCK_WIDTH = int(display_width/self.WIDTH)
        self.BLOCK_HEIGHT = int(display_height/self.HEIGHT)

        #defining agents
        self.CAT = Cat(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOUSE = Mouse(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOVES = {'mouse':150,'cat':150}

        self.OBSTACLES = game_matrix.OBSTACLES

        #and finally the golden cheese
        self.CHEESE_IMG = pygame.transform.scale(pygame.image.load('pics/cheese.png'),
                                                 (self.BLOCK_WIDTH, self.BLOCK_HEIGHT))

#---------------------------------------------Returns the state of the environment----------------------------------#

    def get_state(self):
        
        #later on give cheese state to cat also
        self.STATE = {'mouse':(self.MOUSE_X - self.CAT_X, self.MOUSE_Y - self.CAT_Y,self.MOUSE_X - self.CHEESE_X,self.MOUSE_Y -  self.CHEESE_Y), 
                        'cat':(self.CAT_X - self.MOUSE_X, self.CAT_Y - self.MOUSE_Y)}   

        return self.STATE

#--------------------------------------------Reset the environment--------------------------------------------------#
    
    def reset(self):
        self.MOUSE_X, self.MOUSE_Y = (0,0)
        self.CAT_X, self.CAT_Y = (0, self.HEIGHT -1)
        self.CHEESE_X, self.CHEESE_Y = np.random.randint(0, 9, 2, 'int')

        #making sure cheese is not at obstacles
        for obs in self.OBSTACLES:
            if self.CHEESE_X == obs[0] and self.CHEESE_Y == obs[1]:
                #then shift it up
                    self.CHEESE_Y -= 1

        self.MOVES['cat'] = 100
        self.MOVES['cat'] = 100

        return self.get_state()

#-----------------------------------------------Render the enviroment-----------------------------------------------#    

    def render(self, i_episode=-1):
        '''
            rendering the environment using pygame display
        '''

        #drawing our agents
        self.MOUSE.draw(self.MOUSE_X, self.MOUSE_Y)
        self.CAT.draw(self.CAT_X, self.CAT_Y)
        
        self.DISPLAY.blit(self.CHEESE_IMG, (self.CHEESE_X*self.BLOCK_WIDTH, self.CHEESE_Y*self.BLOCK_HEIGHT))

        #drawing obstacles
        for pos in self.OBSTACLES:
        	pygame.draw.rect(self.DISPLAY, BLUE, [pos[0]*self.BLOCK_WIDTH, pos[1]*self.BLOCK_HEIGHT, self.BLOCK_WIDTH, self.BLOCK_HEIGHT])

        if i_episode>=0:
            self.display_episode(i_episode)

        
#--------------------------------------Agents takes step and the environment changes------------------------------------#

    def step(self,mouse_action, cat_action):

        reward = {'mouse':-1, 'cat':-1}
        done = False
        info = {
            'cheese_eaten': False,
            'mouse_caught': False, 
            'x': -1, 'y': -1, 
            'width':self.BLOCK_WIDTH, 
            'height':self.BLOCK_HEIGHT
        }

        #decreasing the no. of moves
        self.MOVES['cat'] -= 1
        self.MOVES['mouse'] -= 1
        #done if moves = 0
        if self.MOVES['cat'] == 0 or self.MOVES['mouse'] == 0:
            done = True

        self.update_positions(mouse_action, cat_action)
        
        #mouse reached the cheese
        if self.MOUSE_X == self.CHEESE_X and self.MOUSE_Y == self.CHEESE_Y:
            done = True
            reward['mouse'] = 50
            info['cheese_eaten'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y
        
        #cat caught the mouse
        if self.CAT_X == self.MOUSE_X and self.CAT_Y == self.MOUSE_Y:
            done = True
            reward['cat'] = 50
            reward['mouse'] = -20
            info['mouse_caught'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y
        
        for obs in self.OBSTACLES:
            if self.MOUSE_X == obs[0] and self.MOUSE_Y == obs[1]:
                reward['mouse'] = -20
                self.MOUSE_X, self.MOUSE_Y = (0,0)

            if self.CAT_X == obs[0] and self.CAT_Y == obs[1]:    
                reward['cat'] = -20
                self.CAT_X, self.CAT_Y = (0, self.HEIGHT -1)

        return self.get_state(), reward, done, info

            
#----------------------------Helper function to display episode-------------------------#

    def display_episode(self,epsiode):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Episode: "+str(epsiode), True, TEXT_COLOR)
        self.DISPLAY.blit(text,(1,1))		

#-------------------------------Decide position changes based on action taken--------------#


    def get_changes(self, action):
        x_change, y_change = 0, 0

        #decide action
        if action == 0:
            x_change = -1  #moving left
        elif action == 1:
            x_change = 1   #moving right
        elif action == 2:
            y_change = -1 #moving upwards
        elif action ==3:
            y_change = 1  #moving downwards
        
        return x_change, y_change

#-----------------------------update positions of agents-------------------------------------#

    def update_positions(self, mouse_action, cat_action):
        x_change_mouse, y_change_mouse = self.get_changes(mouse_action)
        x_change_cat, y_change_cat = self.get_changes(cat_action)

        self.MOUSE_X += x_change_mouse 
        self.MOUSE_Y += y_change_mouse

        self.CAT_X += x_change_cat 
        self.CAT_Y += y_change_cat 
        
        self.MOUSE_X, self.MOUSE_Y = self.fix(self.MOUSE_X, self.MOUSE_Y)
        self.CAT_X, self.CAT_Y = self.fix(self.CAT_X, self.CAT_Y)

#------------------------------Push them back in to fight! There's no escape--------------------#

    def fix(self, x, y):
        # If agents out of bounds, fix!
        if x < 0:
            x = 0
        elif x > self.WIDTH-1:
            x = self.WIDTH-1
        if y < 0:
            y = 0
        elif y > self.HEIGHT -1:
            y = self.HEIGHT -1

        return x, y


#---- A helpful class GAME_MATRIX (Abstracts the specific features of game from environment)-------------------#


class Game_Matrix:

	def __init__(self, rows=5, columns=5):
		self.ROWS = rows 
		self.COLUMNS = columns
		self.OBSTACLES = [] #[[2,2], [2,7], [7,2], [7,7], [5,5]]

