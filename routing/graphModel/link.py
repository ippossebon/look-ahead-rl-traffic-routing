class Link(object):
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def updateBandwidth(self, new_bandwidth):
        self.weight = new_bandwidth
