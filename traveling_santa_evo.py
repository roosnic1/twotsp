##########################################################################################
##########################################################################################
##                                                                                      ## 
## Dieser Code ist im Rahmen der Projektarbeit des Moduls Softwareprojekt 2             ##
## im Zeitraum vom 20.02.2013 bis 30.05.2013 entstanden.                                ##
##                                                                                      ##
## Authoren: Jeremie Blaser, Nicolas Roos, Martin Eigenmann                             ##
## Version: 1.0                                                                         ##
##                                                                                      ##
## - Alle Rechte Vorbehalten -                                                          ##
##                                                                                      ##
## ------------------------------------------------------------------------------------ ##
## Diese Datei beinhaltet das EVO Objekt zur Findung eines EVO Pfad.                    ##
##                                                                                      ##
##                                                                                      ##
##                                                                                      ##
##                                                                                      ##
##########################################################################################
##########################################################################################

from random import Random
from time import time
from math import cos
from math import pi
from inspyred import ec
import inspyred
from inspyred.ec import terminators
import math
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt
import matplotlib.delaunay as triang
import matplotlib.patches as patch

from traveling_santa_evo_tsp import TSP


class EVO(object):

    def __init__(self, data,route):
        self.route = route
        self.points = []
        for i, p in enumerate(data):
            self.points.insert(i, (np.int_(p[1]) ,np.int_(p[2]) ) )

        self.weights = [[0 for _ in range(len(self.points))] for _ in range(len(self.points))]
        for i, p in enumerate(self.points):
            for j, q in enumerate(self.points):
                self.weights[i][j] = math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)
        


    def calc_path_lenght(self,path):
        total  = 0
        for c in path:
            total += self.weights[c[0]][c[1]]
        return total

    def calc_path_duplicates(self,route0, route1):
        duplicates = 0
        for inx0, edge0 in enumerate(route0):
            for inx1, edge1 in enumerate(route1):
                if( (edge1[0] == edge0[0] and edge1[1] == edge0[1]) or (edge1[1] == edge0[0] and edge1[0] == edge0[1]) ):
                    duplicates += 1
        return duplicates

    def solve(self, display=True):
        prng = Random()
        prng.seed(time()) 
                      
        problem = TSP(self.weights,self.route)

        ea = ec.EvolutionaryComputation(prng)
        ea.selector = ec.selectors.tournament_selection
        ea.variator = [ec.variators.partially_matched_crossover, 
                       ec.variators.inversion_mutation]
        ea.replacer = ec.replacers.generational_replacement
        ea.terminator = ec.terminators.generation_termination
        final_pop = ea.evolve(generator=problem.generator, 
                              evaluator=problem.evaluator, 
                              bounder=problem.bounder,
                              maximize=problem.maximize, 
                              pop_size=200, 
                              max_generations=80,
                              tournament_size=10,
                              num_selected=100,
                              num_elites=5)

        best = max(ea.population)
        self.tour = []
        for i, p in enumerate(best.candidate):
            self.tour.insert(i, (best.candidate[i-1] , p) )

        #print('Best Solution:')
        total = 0
        for c in self.tour:
            total += self.weights[c[0]][c[1]]

        #print('Distance: {0}'.format(total))

        #print('Tour:  ' , self.tour)
        #print('Route: ' , self.route )
        
        return ea