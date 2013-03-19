from random import Random
from time import time
import math
import inspyred
import matplotlib.pyplot as plt
import numpy as np

class EVO(object):

    def __init__(self, data):
        self.points = data
        self.x = self.points[0::, 1].astype(np.float)
        self.y = self.points[0::, 2].astype(np.float)

    def solve(self):
        points = self.points  
        prng = Random()
        prng.seed(time()) 

        weights = [[0 for _ in range(len(points))] for _ in range(len(points))]
        for i, p in enumerate(points):
            for j, q in enumerate(points):
                weights[i][j] = math.sqrt( ( int(p[1]) - int(q[1]) )**2 + ( int(p[2]) - int(q[2]) ) **2)
                  
        problem = inspyred.benchmarks.TSP(weights)
        ac = inspyred.swarm.ACS(prng, problem.components)
        ac.terminator = inspyred.ec.terminators.generation_termination
        final_pop = ac.evolve(generator=problem.constructor, 
                              evaluator=problem.evaluator, 
                              bounder=problem.bounder,
                              maximize=problem.maximize, 
                              pop_size=10, 
                              max_generations=50)
        
        self.best = max(ac.archive)
        self.best_tour_len = (1/self.best.fitness)
        print('Best Distance: {0}'.format(self.best_tour_len))


    def plot(self, labelNodes=False, showMST=False):
        for b in self.best.candidate:
            self.plot_path( b.element )

        plt.plot(self.x, self.y, '.', ms=3)
        plt.axis('equal')
        plt.show()

    def plot_path(self, e):
        x0 = self.x[e[0]]
        x1 = self.x[e[1]]
        dx = x1 - x0
        y0 = self.y[e[0]]
        y1 = self.y[e[1]]
        dy = y1 - y0
        arr = plt.arrow(x0,y0,dx,dy, shape='full', lw=4, color="g",length_includes_head=True, head_width=140, head_length=160, overhang=0, zorder=10, alpha=0.5)
