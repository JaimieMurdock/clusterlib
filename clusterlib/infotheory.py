"""
Implementation of information-theoretic clustering (Gokcay & Principe 2002)

Hill-climbing algorithm
"""

class Concept(object):
    """
    Simple wrapper for a concept that tracks its category assignments. 
    This data structure is used for KNN clustering.
    """

    # initialize the wrapper
    def __init__(self, value):
        self.value = value
        self.cluster = None 
        self.group = [self]

    # Python syntax sugar for string printing
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)

    def make_group(self, population, size):
        """
        Create the group form the population
        """
        # initialize the group
        self.group = [self]

        # create a deep copy of the population
        population = population[:]
        population.remove(self)

        # while there are still things left to cluster, cluster
        for i in range(size):
            # find x, such that distance to any 1 point is minimized.
            # differs from QT Clust, which minimizes whole cluster diameter.
            x = min(population, key=self._diameter_append)
            
            # add to the group
            self.group.append(x)
            population.remove(x)
    
    def _diameter_append(self, candidate):
        return min([distance(candidate.value, x.value) 
                       for x in self.group])

# perform grouping algorithm in which cluster elements selected by the closest
# to any in group, not necessarily closest to prototype
def info_theory(k, population):
    """
    An implementation of the hillclimbing information theoretic approach in
    Gokcay & Principe 2002
    """
    # assign random clusters
    for x in population:
        x.cluster = random.choice(range(k))

    # create initial group size
    group_size = len(population) / k
   
    # grow group size exponentially while hill-climbing
    while group_size < len(population):
        hillclimb(population, group_size)
        group_size *= 2

    return population

def hillclimb(population, group_size):
    # assign groups
    for x in population:
        x.make_group(population, group_size)

    # get baseline CEF
    orig_CEF = CEF(get_clusters())
    min_CEF = 1.0

    # change each group cluster assignment to see if CEF decreases
    # if CEF does not decrease, change second additional group
    # if CEF still does not decrease, move to next group
    # else, record as new minimum assignent
    while orig_CEF != min_CEF:
        for x in population:
            for member in x.group:
                member.cluster = x.cluster
    
            group_CEF = CEF(get_clusters())
            if group_CEF < min_CEF:
                # new min_CEF
                min_CEF = group_CEF
            else:
                # TODO: implement second stage hill-climbing
                # restore previous cluster assignment
                for member in x.group:
                    member.cluster = x.previous_cluster

        # reset the original CEF to the new minima
        orig_CEF = min_CEF

def get_clusters(k, population):
    return [[x for x in population if x.cluster == cluster] 
                   for cluster in range(k)]

def CEF(clusters):
    """
    Cross-entropy function for all groups
    """
    raise NotImplementedError
