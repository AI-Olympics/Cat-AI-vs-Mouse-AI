#The Q-agent class can be extended to child classes

from collections import defaultdict
import sys
import numpy as np 
import pickle
import random

class Q_Agent:

    def __init__(self, env, alpha, nA, gamma=1.0, eps_start=1.0, eps_decay=0.9999, eps_min=0.05):
        self.env = env
        self.eps_start = eps_start
        self.gamma = gamma
        self.alpha = alpha
        self.eps_decay = eps_decay
        self.eps_min = eps_min
        self.nA = nA
        self.Q = defaultdict( lambda: np.zeros(self.nA))  #The Q-TABLE


#---------------------------gets a Greedy action----------------------------------------------------#

    def greedy_action(self, state, epsilon):
        '''
            Chooses the best possible action with a probability of 1-epsilon, or random action
        '''

        prob = random.random()
        if prob > epsilon:
            return np.argmax(self.Q[state])
        else:
            return np.random.choice(np.arange(self.nA))


#---------------------------Learn from the environment----------------------------------------------------#

    def learn(self, state, action, reward, next_state):
        '''
            updates the Q-table
        ''' 
        self.Q[state][action] += self.alpha*(reward + self.gamma*np.max(self.Q[next_state]) - self.Q[state][action])


#---------------------Call this after learning to set a concrete policy-------------------------------------#                
    
    def set_policy(self):
        '''
            sets the optimal policy of agent
        '''
        policy = defaultdict(lambda: 0)
        for state, action in self.Q.items():
            policy[state] = np.argmax(action)
        self.policy = policy
    
#-----------------------------------Take action------------------------------------------------------------#

    def take_action(self,state):
        '''
            take action as per policy
        '''
        return self.policy[state]


#------------------------------------Load saved policies---------------------------------------------------#

    def change_policy(self, directory):
        '''
            To be used while loading saved policies
        '''
        with open(directory, 'rb') as f:
            policy_new = pickle.load(f)
        self.policy = defaultdict(lambda:0, policy_new)  #saved as defaultdict
        print('policy Loaded')        

#------------------------------------Save agent's policy----------------------------------------------------#

    def save(self,i):
        try:
            policy = dict(self.policy)
            with open(f'policy{i}.pickle','wb') as f:
                pickle.dump(policy, f)
        except :
            print('not saved')