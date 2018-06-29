"""
Template for implementing QLearner  (c) 2015 Tucker Balch
Jaswanth Sai Pyneni
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        self.Q = np.zeros((num_states, num_actions), dtype=float)

        if self.dyna != 0:
            self.probList = []


    def author(self):
        return 'jpyneni3'


    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        if rand.random <= self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.Q[s, :])
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        prevState = self.s
        prevAction = self.a
        if self.dyna != 0:
            learningTuple = (prevState, prevAction, s_prime, r)
            self.probList.append(learningTuple)
        self.Q[prevState, prevAction] = (1 - self.alpha) * self.Q[prevState, prevAction] + self.alpha*(r + self.gamma * np.max(self.Q[s_prime, :]))
        if rand.random <= self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.Q[s_prime, :])
        self.rar = self.rar * self.radr

        if self.dyna != 0:
            for i in range(0, self.dyna):
                hallucinate = rand.choice(self.probList)
                hallS = hallucinate[0]
                hallA = hallucinate[1]
                hallNS = hallucinate[2]
                hallR = hallucinate[3]
                self.Q[hallS, hallA] = (1 - self.alpha) * self.Q[hallS, hallA] + self.alpha*(hallR + self.gamma * np.max(self.Q[hallNS, :]))
        self.s = s_prime
        self.a = action
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
