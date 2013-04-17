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
        self.points = []
        for i, p in enumerate(data):
            self.points.insert(i, (np.int_(p[1]) ,np.int_(p[2]) ) )

        #print self.points
        #self.points = [(110.0, 225.0), (161.0, 280.0), (325.0, 554.0), (490.0, 285.0), 
        #      (157.0, 443.0), (283.0, 379.0), (397.0, 566.0), (306.0, 360.0), 
        #      (343.0, 110.0), (552.0, 199.0)]            
        #self.x = data[0::, 1].astype(np.float)
        #self.y = data[0::, 2].astype(np.float)
        self.route = route


        #self.build_mesh()
        #self.build_distance_graph()
        #self.distance_route0 = self.calc_path_length(route0)
        #self.distance_route1 = self.calc_path_length(route1)

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
                    #print('duplicate ({0}) {1} and ({2}) {3}'.format(inx0, edge0, inx1, edge1))
                    duplicates += 1
        return duplicates

    def solve(self, display=True):
        prng = Random()
        prng.seed(time()) 

        #print('weights: ', self.weights)
    
        self.weights = [[0 for _ in range(len(self.points))] for _ in range(len(self.points))]
        for i, p in enumerate(self.points):
            for j, q in enumerate(self.points):
                self.weights[i][j] = math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)
                  
        problem = TSP(self.weights,self.route)
        ac = inspyred.swarm.ACS(prng, problem.components)
        ac.terminator = inspyred.ec.terminators.generation_termination
        final_pop = ac.evolve(generator=problem.constructor, 
                              evaluator=problem.evaluator, 
                              bounder=problem.bounder,
                              maximize=problem.maximize, 
                              pop_size=10, 
                              max_generations=5)

                              
        best = max(ac.archive)
        self.tour = []
        for i, p in enumerate(best.candidate):
            self.tour.insert(i, p.element )
        self.tour.append((p.element[1],self.tour[0][0]) )


        # douplicates = 0
        # for t in self.tour:
        #     for b in self.route:
        #         if( (b[0] == t[0] and b[1] == t[1]) or (b[1] == t[0] and b[0] == t[1]) ):
        #             douplicates += 1


        print('Best Solution:')
        # for b in best.candidate:
        #     print(self.points[b.element[0]])
        #     print b.element[0]

        # print(self.points[best.candidate[-1].element[1]])
        # print(best.candidate[-1].element[1])
        total = 0
        for c in best.candidate:
            total += self.weights[c.element[0]][c.element[1]]
        last = (best.candidate[-1].element[1], best.candidate[0].element[0])
        total += self.weights[last[0]][last[1]]


        print('Fitness: {0}'.format(1/best.fitness))
        print('Distance: {0}'.format(total))

        print('Tour:  ' , self.tour)
        print('Route: ' , self.route )
        
        return ac