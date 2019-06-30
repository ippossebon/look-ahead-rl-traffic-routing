class Flow(object):
    def __init__(self, source, target, bandwidth):
        self.source = source
        self.target = target
        self.bandwidth = bandwidth
        self.path = []

    def setPath(self, path):
        self.path = path
    
