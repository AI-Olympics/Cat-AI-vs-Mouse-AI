
#------------------------------Run this to train the agents---------------------------#

import pygame
import pickle
import time
import random
import sys

from Agent import Q_Agent
from Environment import Game_Env, Game_Matrix 
from cat import Cat
from mouse import Mouse

#colours
ORANGE = (255, 165, 0)
GREEN = (0, 150, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)

display_width, display_height = 600, 700

pygame.init()
pygame.display.set_caption('Grid environment')
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

game_matrix = Game_Matrix(rows=10, columns=10)
env = Game_Env(gameDisplay, game_matrix)

#initialising the agents
cat = Q_Agent(env, alpha = 0.1, nA = 4)
mouse = Q_Agent(env, alpha = 0.1, nA = 4)


#helpful function
def show_info(cheese, mouse):
    pygame.draw.rect(gameDisplay, BLACK, [0, 600, 600, 5])
    font = pygame.font.SysFont(None, 40)
    text1 = font.render("Total Cheese Eaten: "+str(cheese), True, GREEN)
    text2 = font.render("Total Mouse Caught: "+str(mouse), True, RED)
    
    gameDisplay.blit(text1,(50,610))
    gameDisplay.blit(text2,(50,655))	

#indicative rectangle to show cheese eaten or mouse caught
def draw_rect(color, x, y, width, height):
    pygame.draw.rect(gameDisplay, color, [x*width, y*height, width, height], 10)
    pygame.display.update()
    time.sleep(2)

total_mouse_caught = 0
total_cheese_eaten = 0

epsilon, eps_decay, eps_min = 1.0, 0.99, 0.05
#number of episodes to train
num_episodes = 3000

# loop over episodes
for i_episode in range(1, num_episodes+1):
    # monitor progress
    if i_episode % 100 == 0:
        print("\rEpisode {}/{}".format(i_episode, num_episodes), end="")
        sys.stdout.flush() 

    epsilon = max(epsilon*eps_decay, eps_min)
    
    state = env.reset()
    action_mouse = mouse.greedy_action(state['mouse'], epsilon)
    action_cat = cat.greedy_action(state['cat'], epsilon)
    
    #render the environment         
    env.render(i_episode)

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   #close the window
                quit() 

        
        next_state, reward, done, info = env.step(action_mouse, action_cat)
        
        #let's teach our agents to do something! hopefully they learn.
        mouse.learn(state['mouse'], action_mouse, reward['mouse'], next_state['mouse'])
        cat.learn(state['cat'], action_cat, reward['cat'], next_state['cat'])
        
        #render the environment
        gameDisplay.fill(WHITE)         
        env.render(i_episode)
        show_info(total_cheese_eaten, total_mouse_caught)

        #updating the display
        pygame.display.update()
        clock.tick(60)
        
        if done:
            if info['cheese_eaten']:
                total_cheese_eaten += 1
                draw_rect(GREEN, info['x'], info['y'], info['width'], info['height'])       
            
            if info['mouse_caught']:
                total_mouse_caught += 1
                draw_rect(RED, info['x'], info['y'], info['width'], info['height'])    
            #finish this episode    
            break
       
        #update state and action
        state = next_state
        action_mouse = mouse.greedy_action(state['mouse'], epsilon)
        action_cat = cat.greedy_action(state['cat'], epsilon)
        

cat.set_policy()
mouse.set_policy()

#to save the policy
cat.save('_cat_5')
mouse.save('_mouse_5')

#once the policy is saved, 
#Load it in the test file and see it in action

