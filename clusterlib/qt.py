"""
Implementation of the QT Clust algorithm (Heyer et al 1999)

Prototype model
"""
import math
import random

from distance import euclidean as distance

class Concept(object):
    """
    Simple wrapper for a concept that tracks its category assignments. 
    This data structure is used for KNN clustering.
    """

    # initialize the wrapper
    def __init__(self, value):
        self.value = value
        self.cluster = [self] 
        self.diameter = 0.0

    # Python syntax sugar for string printing
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)

    def build_cluster(self, population, thresh):
        """
        Create the candidate cluster from the population
        """
        # initialize the cluster
        self.cluster = [self]

        # create a deep copy of the population
        population = population[:]
        population.remove(self)

        # while there are still things left to cluster, cluster
        while population:
            # find x, such that cluster diameter is minimized
            x = min(population, key=self._diameter_append)
            new_diameter = self._diameter_append(x)
            if new_diameter < thresh:
                # add to cluster and remove from population if we are below
                # the quality threshold.
                self.cluster.append(x)
                self.diameter = new_diameter
                population.remove(x)
            else:
                # otherwise terminate the loop
                break
    
    def _diameter_append(self, candidate):
        return max([distance(candidate.value, x.value) 
                       for x in self.cluster])

def qt_clust(thresh, population):
    """
    Implementation of the QT Clust algorithm.
    """
    while population:
        # build candidate clusters
        for x in population:
            x.build_cluster(population, thresh)
    
        # select the largest candidate cluster
        candidate = max(population, key=lambda x: len(x.cluster))
  
        # remove elements from the population
        for x in candidate.cluster:
            population.remove(x)
    
        yield candidate

def distribution(n, d=2):
    """ Generates a random distribution of size n. """
    # autogenerate a mean
    mean = math.log(random.random() * n)

    # autogenerate a stddev
    stddev = math.log(random.random() * n)

    return [[random.normalvariate(mean, stddev + j) for j in range(d)]
                for i in range(n)]

if __name__ == '__main__':
    population = distribution(100) 

    # initialize population with cluster storage representation
    population = [Concept(x) for x in population]

    # cluster the population!
    for prototype in qt_clust(3, population):
        print len(prototype.cluster), prototype
