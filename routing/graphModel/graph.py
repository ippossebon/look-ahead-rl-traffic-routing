class Graph(object):
    def __init__(self):
        self.links = []
        self.nodes = []

    def addLink(self, link):
        self.links.append(link)

    def addNode(self, node):
        self.nodes.append(node)

    def printGraph(self):
        for link in self.links:
            print('{node1}-------({weight})-------{node2}'.format(
                node1=link.node1.name,
                weight=link.weight,
                node2=link.node2.name
            ))
