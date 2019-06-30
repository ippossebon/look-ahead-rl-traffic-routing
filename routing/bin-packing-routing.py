from graphModel.flow import Flow
from graphModel.graph import Graph
from graphModel.link import Link
from graphModel.node import Node

from operator import attrgetter


class BinPackingRouting(object):
    def __init__(self, network):
        self.network = network

    def findPaths(self, flows):
        # Ordena pares de switches de forma decrescente em relação ao volume de
        # tráfego
        flows_copy = list(flows)
        ordered_flows = []
        while len(flows_copy) > 0:
            max_volume_required_item = max(flows_copy, key=attrgetter('bandwidth'))
            ordered_flows.append(max_volume_required_item)
            item_index = flows_copy.index(max_volume_required_item)
            del flows_copy[item_index]

        # Calcula caminho de custo mínimo, onde o custo de cada caminho é o recíproco
        # da sua capacidade disponível (1/capacidade). Após associar um par de
        # switches a um caminho, atualiza o custo de cada link.
        



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
    link15 = Link(node1, node5, 500)
    networkGraph.addLink(link15)
    link23 = Link(node2, node3, 500)
    networkGraph.addLink(link23)
    link25 = Link(node2, node5, 500)
    networkGraph.addLink(link25)
    link34 = Link(node3, node4, 500)
    networkGraph.addLink(link34)
    link45 = Link(node4, node5, 500)
    networkGraph.addLink(link45)
    link46 = Link(node4, node6, 500)
    networkGraph.addLink(link46)
    link56 = Link(node5, node6, 500)
    networkGraph.addLink(link56)

    routingModel = BinPackingRouting(networkGraph)

    flow16 = Flow(node1, node6, 200)
    flow24 = Flow(node2, node4, 50)
    flow36 = Flow(node3, node6, 100)

    flows = []
    flows.append(flow16)
    flows.append(flow24)
    flows.append(flow36)

    paths = routingModel.findPaths(flows)
