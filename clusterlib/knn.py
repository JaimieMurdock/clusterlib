"""
Implementation of the k-means nearest neighbor algorithm.
"""
from __future__ import division
import math
from operator import itemgetter, attrgetter
import random
import subprocess

import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot

from distance import euclidean as distance

class Concept(object):
    """
    Simple wrapper for a concept that tracks its category assignments. 
    This data structure is used for KNN clustering.
    """

    # initialize the wrapper
    def __init__(self, value):
        self.value = value
        self._cluster = None
        self._previous_cluster = None

    # Properties to track cluster assignments
    @property
    def cluster(self):
        return self._cluster
        
    @cluster.setter
    def cluster(self, value):
        """ Track previous cluster assignment auto-magically. """
        self._previous_cluster = self._cluster
        self._cluster = value
    
    @property
    def previous_cluster(self):
        return self._previous_cluster


    # Python syntax sugar for string printing
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)

def kmeans(k, population, min_delta=0):
    """
    Implementation of k-means nearest neighbor algorithm.
    """
    # initialize centroids with random members of the population
    centroids = [random.choice(population).value for i in range(k)]
   
    # delta is the number of elements that switch cluster
    # since all members will be changing on the first round,
    # we initialize delta to the length of the population
    delta = len(population)

    # track how many iterations until convergence
    iterations = 0
    plot(population, k, iterations, centroids)

    # test for convergence
    while delta > min_delta:
        # assign population to centroids
        assign_clusters(population, centroids)

        # update centroids
        centroids = update_centroids(population, centroids)
        
        # get number of elements which switched cluster
        delta = len([x for x in population if x.cluster != x.previous_cluster])
       
        #plot the data
        iterations += 1
        plot(population, k, iterations)

    return population

def assign_clusters(population, centroids):
    """ Cluster assignment step. """
    for x in population:
        # calculate distance to each centroid
        distances = [distance(x.value, centroid) for centroid in centroids]

        # select the index (cluster id) of the closest cluster
        cluster, min_distance = min(enumerate(distances), key=itemgetter(1))

        # assign the object to that cluster
        x.cluster = cluster

    return population

def update_centroids(pouplation, centroids):
    """ Centroid update step. """ 
    # initialize variables
    k = len(centroids)

    return get_centroids(population, k)

def get_centroids(population, k):
    new_centroids = []

    for cluster in range(k): 
        # filter out the cluster population
        cluster_values = [x.value for x in population if x.cluster == cluster]
        # generate the new centroid by taking the average of all exemplars
        # comprising the cluster. First, sum the dimensions:
        centroid = map(sum, zip(*cluster_values))

        # then take the average:
        centroid = [dimension / len(cluster_values) for dimension in centroid]  

        # add to our list of new centroids
        new_centroids.append(centroid)
   
    return new_centroids

def plot(population, k, n, centroids=None):
    """
    Create plot of k-means nearest neighbor clustering process.
    """
    pyplot.title('knn after %d iterations' % n)
    axes = pyplot.axes()

    unchanged = [x for x in population if x.cluster == x.previous_cluster 
                                           and x.cluster is not None]
    if unchanged:
        xs, ys = zip(*map(attrgetter('value'), unchanged))
        cs = [x.cluster / k for x in unchanged]
        axes.scatter(xs, ys, c=cs, cmap='Paired', marker='o', alpha=0.75)

    changed = [x for x in population if x.cluster != x.previous_cluster]
    if changed:
        xs, ys = zip(*map(attrgetter('value'), changed))
        cs = [x.cluster / k for x in changed]
        axes.scatter(xs, ys, s=100, c=cs, cmap='Paired', marker='o', alpha=1.0)
    
    unassigned = [x for x in population if x.cluster is None]
    if unassigned:
        xs, ys = zip(*map(attrgetter('value'), unassigned))
        axes.scatter(xs, ys, c='grey', marker='o', alpha=0.5)

    if centroids is None:
        centroids = get_centroids(population, k)
    cxs, cys = zip(*centroids)
    ccs = range(k)
    axes.scatter(cxs, cys, s=300, c=ccs, cmap='Paired', marker='^')

    # save to file
    pyplot.savefig('plots/%05d.png' % n)

    # clear the axes
    pyplot.cla()


def distribution(n, d=2):
    """ Generates a random distribution of size n. """
    # autogenerate a mean
    mean = math.log(random.random() * n)

    # autogenerate a stddev
    stddev = math.log(random.random() * n)

    return [[random.normalvariate(mean, stddev + j) for j in range(d)]
                for i in range(n)]

if __name__ == '__main__':
    import sys
    random.seed(42)
    population = distribution(1000) 

    # initialize population with cluster storage representation
    population = [Concept(x) for x in population]

    # cluster the population!
    k = int(sys.argv[-1])
    population = kmeans(k, population)
    for i, centroid in enumerate(get_centroids(population, k)):
        print i, centroid

    subprocess.call(("mencoder mf://%s/*.png -o output%d.avi -mf type=png:w=800:h=600:fps=3 -ovc x264 -x264encopts qp=20" % ('plots', k) ).split())

