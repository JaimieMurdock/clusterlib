"""
Representations of concepts and populations.
"""


class Concept(object):
    """
    Simple wrapper for a concept that tracks its category assignments.
    """

    def __init__(self, obj):
        self.obj = obj
        self.cluster = None
        self.previous_cluster = None

    @cluster.setter
    def cluster(self, value):
        """
        Custom setter for the cluster property, tracks previous cluster.
        """
        self.previous_cluster = self.cluster
        self.cluster = value
