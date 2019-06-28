from graphModel.graph import Graph
from graphModel.link import Link
from graphModel.node import Node

class BinPackingRouting(object):
    def __init__(self, network):
        self.network = network

    def run(self):
        self.network.printGraph()

if __name__ == '__main__':
    networkGraph = Graph()

    node1 = Node(name='S1')
    networkGraph.addNode(node1)
    node2 = Node(name='S2')
    networkGraph.addNode(node2)
    node3 = Node(name='S3')
    networkGraph.addNode(node3)
    node4 = Node(name='S4')
    networkGraph.addNode(node4)
    node5 = Node(name='S5')
    networkGraph.addNode(node5)
    node6 = Node(name='S6')
    networkGraph.addNode(node6)

    link12 = Link(node1, node2, 500)
    networkGraph.addLink(link12)
    link13 = Link(node1, node3, 500)
    networkGraph.addLink(link13)
    link24 = Link(node2, node4, 500)
    networkGraph.addLink(link24)
    link34 = Link(node3, node4, 500)
    networkGraph.addLink(link34)
    link45 = Link(node4, node5, 500)
    networkGraph.addLink(link45)
    link46 = Link(node4, node6, 500)
    networkGraph.addLink(link46)
    link56 = Link(node5, node6, 500)
    networkGraph.addLink(link56)

    routingModel = BinPackingRouting(networkGraph)
    routingModel.run()
