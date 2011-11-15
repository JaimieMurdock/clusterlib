"""
Implementation of the k-means nearest neighbor algorithm.
"""
import random
import operator

def kmeans(k, population, min_delta=0):
    """
    Implementation of k-means nearest neighbor algorithm.
    """
    # initialize centroids with random members of the population
    centroids = [random.choice(population) for i in range(k)]

    # initialize population with cluster storage representation
    population = [Concept(x) for x in population]
   
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
        centroids = update_centroids(centroids, population)

    return population

def assign_clusters(population, centroids):
    """ Cluster assignment step. """
    for x in population:
        # calculate distance to each centroid
        distances = [distance(x.obj, centroid) for centroid in centroids]

        # select the index (cluster id) of the closest cluster
        cluster, distance = min(enumerate(distances), key=itemgetter(1))

        # assign the object to that cluster
        x.cluster = cluster

    return population

def update_centroids(pouplation, centroids):
    """ Centroid update step. """ 
    # initialize variables
    k = len(centroids)
    new_centroids = []

    for cluster in range(k): 
        # filter out the cluster population
        cluster_pop = [x for x in population if x.cluster == cluster]

        # generate the new centroid by taking the average of all exemplars
        # comprising the cluster. First, sum the dimensions:
        centroid = map(sum, zip(cluster_pop))
        # then take the average:
        centroid = [dimension / len(cluster_pop) for dimension in centroid]  

        # add to our list of new centroids
        new_centroids.append(centroid)
   
    return new_centroids

