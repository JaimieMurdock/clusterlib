"""
Representations of concepts and populations.
"""


class Concept(object):
    """
    Simple wrapper for a concept that tracks its category assignments.
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
