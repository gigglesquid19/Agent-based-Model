# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 10:22:29 2021

@author: Ciaran
"""
# Import Modules
import matplotlib.animation as animation
import csv
import sys
import time
import random
import agentframework3
import matplotlib.pyplot as pyplot
import numpy as np
from bs4 import BeautifulSoup
import requests


# GenF data steam to animate function until stopping condition met    
def gen_function(b = [0]):
    a = 0
    global carry_on 
    while (carry_on == True):
        yield a		
        a = a + 1


# Global Variables
carry_on = True
environment = []
deers = []
wolves = []


# Use Cases
num_of_deers = int(input("Please Enter the no. of deer: "))
num_of_wolves = int(input("Please Enter the no. of wolves: "))
num_of_iter = int(input("Please Enter the no. of model interactions: "))
if num_of_iter not in range(100, 500):
    sys.exit("Please enter a no. of model iterations between 100-500")
neighbourhood = int(input("Please Enter a neighborhood value: "))
if neighbourhood not in range(10, 100):
    sys.exit("Please enter a neighbourhood value between 10-100")
    
    
# Define Scatter Plot
fig = pyplot.figure(figsize=(7, 7))
ax = pyplot.axes(xlim=(0, 100), ylim=(0, 100))
deer_plot = pyplot.scatter([], [], color='g')
wolf_plot = pyplot.scatter([], [], color='w')
ax.set_autoscale_on(False)
tic = time.perf_counter()


# Requests data from web, parses html into lists of x + y classes
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})


# Opens csv file into reader, appends values to rowlist, rowlists to env
with open('in.txt', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        rowlist = []
        environment.append(rowlist)
        for values in row:
            i = int(values)
            rowlist.append(i)
            
    # Create the background
    background = pyplot.imshow(environment)

    # Create the Deer + print coordinates
    for i in range(num_of_deers):
        y = int(td_ys[i].text)
        x = int(td_xs[i].text)
        deers.append(agentframework3.Deer(i, y, x, environment))
        print("Deer Coordinates..." + str(deers[i]._y), str(deers[i]._x))
        
    # Create the Wolves and print coordinates
    for l in range(num_of_wolves):
        wolves.append(agentframework3.Wolf(i))
        print("Wolf Coordinates..." + str(wolves[l]._x), str(wolves[l]._y))

    # Loop through deers, pop lists of deers they are aware of
    for deer in deers:
        deer.pop_deers(deers)
    
    # Loop through wolves, pop lists of deers and other wolves aware of
    for wolf in wolves:
        wolf.pop_deers(deers)
        wolf.pop_wolves(wolves)
     
        
    # Updates the plot at each frame
    def animate(frame_number):

        # Randomize the list of deers to mitigate against model artifacts
        random.shuffle(wolves)
        random.shuffle(deers)

        # Define Deer lists
        deerxpos = []
        deerypos = []
        deercolors = []
        
        # Define Wolf lists
        wolfxpos = []
        wolfypos = []
        wolfcolors = []
        
        # Loop through deers and call their methods for a model iteration
        for i in range(len(deers)):
            deers[i].move()
            deers[i].eat()
            deers[i].share_with_neighbours(neighbourhood)
            # Append deer x + y positions to relevant lists
            deerxpos.append(deers[i]._x)
            deerypos.append(deers[i]._y)
            deercolors.append(deers[i].color)
        
        
        # Loop through wolves + call methods, if eaten, remove deer by index
        for l in range(len(wolves)):
            wolves[l].move()
            index = wolves[l].eat(neighbourhood)
            if index != -1:
                print(f"Removing deer index {index}", flush=True)
                deers.pop(index)
                deerxpos.pop(index)
                deerypos.pop(index)
                deercolors.pop(index)
            
                
            # If energy depleted, wolf rem. All wolves starved stops program
            index1 = wolves[l].starve()
            if index1 != -1:
                wolves.pop(index1)
                print(f"Removing wolf index {index1}", flush=True)
                print(len(wolves))
                if len(wolves) < 1:
                    print("Stopping Condition")
                    toc = time.perf_counter()
                    print(f"Model ran in {toc - tic:0.4f} seconds", flush=True)
                    global carry_on
                    carry_on = not carry_on
                wolfxpos.pop(index1)
                wolfypos.pop(index1)
                wolfcolors.pop(index1)
                
            # Append wolf x + y positions to relevant lists
            wolfxpos.append(wolves[l]._x)
            wolfypos.append(wolves[l]._y)
            wolfcolors.append(wolves[l].color)
            
        
        # Set scatter background as environment list
        background.set_array(environment)
        
        
        # Create lists of XY deer + XY wolf coordinates and plot to scatter
        deer_plot.set_offsets(np.array(list(zip(deerxpos, deerypos))))
        wolf_plot.set_offsets(np.array(list(zip(wolfxpos, wolfypos))))
        deer_plot.set_array(np.array(deercolors))
        wolf_plot.set_array(np.array(wolfcolors))
        return deer_plot, wolf_plot
    


# Makes an animation by repeatedly calling function Func
animation = animation.FuncAnimation(fig, animate, interval=250, 
                                    frames=gen_function, repeat=False)

pyplot.show()
