"""
Implementation of the QT Clust algorithm (Heyer et al 1999)

Prototype model
"""
from __future__ import division
import math
from operator import attrgetter
import random
import subprocess

import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot
from matplotlib.colors import Normalize

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

def plot(population, prototype=None, iteration=0, total=1):
    """
    Create plot of qt-clust clustering process
    """
    pyplot.title('qt after %d iterations' % iteration)
    axes = pyplot.axes()

    if prototype is None:
        xs, ys = zip(*map(attrgetter('value'), population))
        axes.scatter(xs, ys, c='grey', marker='o', alpha=0.5)

    else:
        xs, ys = zip(*map(attrgetter('value'), population))
        color = iteration / total
        print color
        cs =  [color for x in population]
        #plot population
        axes.scatter(xs, ys, c=cs, cmap='Paired', marker='o', norm=Normalize(0, 1))
        #plot prototype
        axes.scatter([prototype.value[0]], [prototype.value[1]], s=100,
                     c=[color], cmap='Paired', marker='o', norm=Normalize(0, 1))
        
        #plot centroid
        cluster_values = [x.value for x in population]
        # generate the new centroid by taking the average of all exemplars
        # comprising the cluster. First, sum the dimensions:
        centroid = map(sum, zip(*cluster_values))

        # then take the average:
        centroid = [dimension / len(cluster_values) for dimension in centroid]  
        axes.scatter([centroid[0]], [centroid[1]], s=200,
                     c=[color], cmap='Paired', marker='^', norm=Normalize(0, 1))

    # save to file
    pyplot.savefig('plotsqt/%05d.png' % iteration)

stddev = 3

def distribution(n, d=2):
    """ Generates a random distribution of size n. """
    # autogenerate a mean
    mean = math.log(random.random() * n)

    # autogenerate a stddev
    global stddev
    stddev = math.log(random.random() * n)

    return [[random.normalvariate(mean, stddev + j) for j in range(d)]
                for i in range(n)]

if __name__ == '__main__':
    import sys
    random.seed(42)
    population = distribution(100) 

    # initialize population with cluster storage representation
    population = [Concept(x) for x in population]
    plot(population)

    # cluster the population!
    thresh = float(sys.argv[-1])
    clusters = list(qt_clust(thresh*stddev, population))
    for i, prototype in enumerate(clusters):
        print len(prototype.cluster), prototype
        plot(prototype.cluster, prototype, i, len(clusters))
    
    subprocess.call(("mencoder mf://%s/*.png -o output_qt%f.avi -mf type=png:w=800:h=600:fps=3 -ovc x264 -x264encopts qp=20" % ('plotsqt', thresh) ).split())

