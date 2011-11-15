"""
Implementation of the k-means nearest neighbor algorithm.
"""
import math
from operator import itemgetter, attrgetter
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

    # test for convergence
    while delta > min_delta:
        # assign population to centroids
        assign_clusters(population, centroids)
        
        # get number of elements which switched cluster
        delta = len([x for x in population if x.cluster != x.previous_cluster])

        # update centroids
        centroids = update_centroids(population, centroids)

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

def distribution(n, d=2):
    """ Generates a random distribution of size n. """
    # autogenerate a mean
    mean = math.log(random.random() * n)

    # autogenerate a stddev
    stddev = math.log(random.random() * n)

    return [[random.normalvariate(mean, stddev + j) for j in range(d)]
                for i in range(n)]

if __name__ == '__main__':
    population = distribution(1000) 

    # initialize population with cluster storage representation
    population = [Concept(x) for x in population]

    # cluster the population!
    population = kmeans(3, population)
    for i, centroid in enumerate(get_centroids(population, 3)):
        print i, centroid
