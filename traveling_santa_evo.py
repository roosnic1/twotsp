from random import Random
from time import time
from math import cos
from math import pi
from inspyred import ec
from inspyred.ec import terminators
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt
import matplotlib.delaunay as triang
import matplotlib.patches as patch


class EVO(object):

    def __init__(self, data,route0,route1):
        self.points = data
        self.x = self.points[0::, 1].astype(np.float)
        self.y = self.points[0::, 2].astype(np.float)
        self.route0 = route0
        self.route1 = route1

        self.build_mesh()
        self.build_distance_graph()
        self.distance_route0 = self.calc_path_length(route0)
        self.distance_route1 = self.calc_path_length(route1)


    def generate(random, args):
        return self.route0


    def evaluate(candidates, args):
        fitness = []
        for cs in candidates:
            fit = self.calc_path_length(cs)
            fitness.append(fit)
        return fitness

    def solve(self, display=True):
        prng = Random()
        prng.seed(time()) 
    
        ea = ec.EvolutionaryComputation(prng)
        ea.selector = ec.selectors.tournament_selection
        ea.replacer = ec.replacers.crowding_replacement
        ea.variator = ec.variators.gaussian_mutation
        ea.terminator = ec.terminators.evaluation_termination

        final_pop = ea.evolve(self.generate, self.evaluate, pop_size=30, 
                              bounder=ec.Bounder(0, 26),
                              max_evaluations=10000,
                              num_selected=30,
                              mutation_rate=1.0,
                              crowding_distance=10)
                              
        if display:
            import pylab
            x = []
            y = []
            for p in final_pop:
                x.append(p.candidate[0])
                y.append(math.sin(p.candidate[0]))
            t = [(i / 1000.0) * 26.0 for i in range(1000)]
            s = [math.sin(a) for a in t]
            pylab.plot(t, s, color='b')
            pylab.scatter(x, y, color='r')
            pylab.axis([0, 26, 0, 1.1])
            pylab.savefig('niche_example.pdf', format='pdf')
            pylab.show()
        return ea
        



# Copy from traveling_santa.py
    def calc_path_length(self, path):
        plen = 0
        for i, j in path:
            plen += self.g.dist_func(i, j)
        return plen

    def build_distance_graph(self):
        print "build graph"
        self.xy = np.array((self.x, self.y))
        g = nx.Graph()
        g.dist_func = self.euclidean_dist
        for i, j in self.edges:
            g.add_edge(i, j, weight=g.dist_func(i, j))
        self.g = g
        print '#edges:', len(self.edges), '#nodes:', len(self.x)
    
    def euclidean_dist(self, i, j):
        d = self.xy[:,i] - self.xy[:,j]
        return np.sqrt(np.dot(d, d))

    def build_mesh(self):
        print 'triangulating ...'
        circumcenters, edges, tri_points, tri_neighbors = triang.delaunay(self.x, self.y)
        self.tri_points = tri_points
        self.edges = edges