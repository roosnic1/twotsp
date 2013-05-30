import copy
from inspyred import ec
from inspyred.ec import emo
from inspyred.ec import selectors
from inspyred import swarm
import itertools
import math
import random


class TSP(object):
  
    def __init__(self, weights, route):
        self.route = route
        self.weights = weights
        self.components = [swarm.TrailComponent((i, j), value=(1 / weights[i][j])) for i, j in itertools.permutations(range(len(weights)), 2)]
        self.bias = 0.5
        self.bounder = ec.DiscreteBounder([i for i in range(len(weights))])
        self.maximize = True
        self._use_ants = False
        
    def __repr__(self):
        return self.__class__.__name__

        
    def __call__(self, *args, **kwargs):
        candidate = [a for a in args]
        fit = self.evaluator([candidate], kwargs)
        return fit[0]

    # Generation eines einzelnen Kandidaten
    def generator(self, random, args):
        """Return a candidate solution for an evolutionary computation."""
        locations = [i for i in range(len(self.weights))]
        random.shuffle(locations)
        return locations
    # Generation eines einzelnen Kandidaten
    def constructor(self, random, args):
        self._use_ants = True
        """Return a candidate solution for an ant colony optimization."""
        candidate = []
        while len(candidate) < len(self.weights) - 1:
            # Find feasible components
            feasible_components = []
            if len(candidate) == 0:
                feasible_components = self.components
            elif len(candidate) == len(self.weights) - 1:
                first = candidate[0]
                last = candidate[-1]
                feasible_components = [c for c in self.components if c.element[0] == last.element[1] and c.element[1] == first.element[0]]
            else:
                last = candidate[-1]
                already_visited = [c.element[0] for c in candidate]
                already_visited.extend([c.element[1] for c in candidate])
                already_visited = set(already_visited)
                feasible_components = [c for c in self.components if c.element[0] == last.element[1] and c.element[1] not in already_visited]
            if len(feasible_components) == 0:
                candidate = []
            else:
                # Choose a feasible component
                if random.random() <= self.bias:
                    next_component = max(feasible_components)
                else:
                    next_component = selectors.fitness_proportionate_selection(random, feasible_components, {'num_selected': 1})[0]
                candidate.append(next_component)
        return candidate
    
    def evaluator(self, candidates, args):
#opt
        """Return the fitness values for the given candidates."""
        fitness = [0 for _ in range(len(candidates))]
        douplicates = 1
        if self._use_ants :
            for inx, candidate in enumerate(candidates):
                total = 0
                for c in candidate:
                    total += self.weights[c.element[0]][c.element[1]]
                    #find duplicated edges
                    for b in self.route:
                        if( (b[0] == c.element[0] and b[1] == c.element[1]) or (b[1] == c.element[0] and b[0] == c.element[1]) ):
                            #douplicates += 1
                            total += self.weights[c.element[0]][c.element[1]]#*douplicates
                            
                last = (candidate[-1].element[1], candidate[0].element[0])
                total += self.weights[last[0]][last[1]]
                fitness[inx] = ( 1 / total )
        else:
            
            for candidate in candidates:
                total = 0
                for src, dst in zip(candidate, candidate[1:] + [candidate[0]]):
                    total += self.weights[src][dst]
                fitness.append(1 / total)


        return fitness