import math

def euclidean(x, y):
    """ Calculates the euclidean distance for arbitrary dimensionality """
    dist = sum([(a - b) ** 2 for a, b in zip(x, y)])
    return math.sqrt(dist) 
