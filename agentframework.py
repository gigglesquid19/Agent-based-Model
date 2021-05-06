# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 10:38:23 2021

@author: Ciaran
"""
import random

class Deer:
    '''
        A Class to represent the Deer Agents
    '''
    def __init__(self, i, y, x, environment):
        '''
            Creates the variables associated with the Class Deer

        Parameters
        ----------
        i : TYPE INT
            DESCRIPTION. The ID number of the agent
        y : TYPE INT
            DESCRIPTION. The Y coordinate of the agent from web
        x : TYPE INT
            DESCRIPTION. The X coordinate of the agent from web
        environment : TYPE LIST
            DESCRIPTION. A list of pixel RGB values
        '''
        
        if (x == None):
            self._x = random.randint(0,100)
        else:
            self._x = x
            
        if (y == None):
            self._x = random.randint(0,100)
        else:
            self._y = y
        
        self.environment = environment
        self.store = 0
        self.color = 1
        self.deers = []
        self.wolves = []
        self.id = id
            
    def pop_deers(self, deers):
        '''
            Populates the list of deers that a specific deer is aware of
        '''
        self.deers = deers
        
    # Property X Functions    
    def getx(self):
        return self._x
    
    def setx(self, value):
        self._x = value
     
    def delx(self):
        del self._x
    x = property(getx, setx, delx)
        
    
    # Property Y Functions
    def gety(self):
        return self._y
     
    def sety(self, value):
        self._y = value
        
    def dely(self):
        del self._y  
    y = property(gety, sety, dely)
    
    # 
    def move(self):
        '''
            Generates x2 random numbers which determine movement direction
        '''
        if random.random() < 0.33:
            self._y = (self._y + 1) % 100
        else:
            self._y = (self._y - 1) % 100
    
        if random.random() < 0.33:
            self._x = (self._x + 1) % 100
        else:
            self._x = (self._x - 1) % 100
            
    
    def eat(self):
        '''
            As long as environment square has a value, eat portion and store
        '''
        if self.environment[self._y][self._x] > 0:
            self.environment[self._y][self._x] -= 10
            self.store += 10
            
            
    def distance_between(self, deer):
        '''
            Calculates the Euclidean Distance between each deer agent
            
        Parameters
        ----------
        deer : TYPE INT
            DESCRIPTION. Individual Deer no. from the list Deers

        Returns
        -------
        TYPE FLOAT
            DESCRIPTION. Euclidean Distance

        '''
        return (((self._x - deer._x)**2) + ((self._y - deer._y)**2))**0.5
    
    
    # Check deer proximity, if less than neighborhood, combine, average and re-distr
    def share_with_neighbours(self, neighbourhood):
        for deer in self.deers:
            dist = self.distance_between(deer)
            if dist <= neighbourhood and dist != 0:
                sum = self.store + deer.store
                average = sum/2
                self.store = average
                deer.store = average
                print("Deer proximity: " + str(dist) + 
                      " New Deer Store: " + str(average))
        
                
class Wolf:
    '''
        A Class to represent the Wolf Agents
    '''
    def __init__(self, i):
        '''
            Creates the variables associated with the Class Wolves

        Parameters
        ----------
        i : TYPE INT
            DESCRIPTION. The ID number of the agent
        '''
        self._x = random.randint(0,99)
        self._y = random.randint(0,99)
        self.store = 0
        self.color = 1
        self.deers = []
        self.wolves = []
        self.energy = 200
        self.id = id
        
       
    def pop_deers(self, deers):
        '''
            Populates the list of deers that a specific wolf is aware of
            
            Parameters
        ----------
        deers : TYPE List
            DESCRIPTION. The list of deer agents
        '''
        self.deers = deers
    
    def pop_wolves(self, wolves):
        '''
            Populates the list of wolves that a specific wolf is aware of
        Parameters
        ----------
        wolves : TYPE List
            DESCRIPTION. The list of wolf agents
        '''
        self.wolves = wolves
        
    

    def move(self):
        '''
            Generates x2 random numbers which determine movement direction
            while determining the energy cost of the movement
        '''
        if random.random() < 0.33:
            self._y = (self._y + 4) % 100
            self.energy = self.energy - 1
        else:
            self._y = (self._y - 4) % 100
            self.energy = self.energy - 1
    
        if random.random() < 0.33:
            self._x = (self._x + 4) % 100
            self.energy = self.energy - 1
        else:
            self._x = (self._x - 4) % 100
            self.energy = self.energy - 1
            
        
    # Loop through individual wolf lists of deer prox, if close enough, remove deer and restore Wolf energy
    def eat(self, neighbourhood):
        for deer in self.deers:
            dist = self.distance_between(deer)
            if dist <= neighbourhood and self.energy <= 100:
                print(f"Eating deer - pos {self.deers.index(deer)}", flush=True)
                self.energy = 150
                print("Wolf Energy restored")
                # Return index of deer eaten or -1 if nothing eaten
                return self.deers.index(deer)
        return -1
        
                
    def distance_between(self, deer):
        '''
            Calculates the Euclidean Distance between wolf and each deer agent
            
        Parameters
        ----------
        deer : TYPE INT
            DESCRIPTION. Individual Deer no. from the list Deers

        Returns
        -------
        TYPE FLOAT
            DESCRIPTION. Euclidean Distance
        '''
        return (((self._x - deer._x)**2) + ((self._y - deer._y)**2))**0.5
    
    
    # Loop through individual wolf lists, if energy depleted remove starved wolf
    def starve(self):
        for wolf in self.wolves:
            if self.energy <= 0:
                print(f"Wolf Energy depleted - pos {self.wolves.index(wolf)}",
                      flush=True)
                # Return index of the starved wolf or -1 if none starved
                return self.wolves.index(wolf)
        return -1
            
    
    
            
            
            
            
            
            
            
