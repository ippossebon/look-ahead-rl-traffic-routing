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

        # ordered_flows contém a lista de pares de switches ordenados por volume
        # de tráfego necessário

        # Calcula caminho de custo mínimo, onde o custo de cada caminho é o recíproco
        # da sua capacidade disponível (1/capacidade). Após associar um par de
        # switches a um caminho, atualiza o custo de cada link.
        for flow in ordered_flows:
            min_cost_path = self.network.getMinimumCostPath(flow)



if __name__ == '__main__':
    nodes = []
    links = []

    node0 = Node(name='S0', index=0)
    nodes.append(node0)
    node1 = Node(name='S1', index=1)
    nodes.append(node1)
    node2 = Node(name='S2', index=2)
    nodes.append(node2)
    node3 = Node(name='S3', index=3)
    nodes.append(node3)
    node4 = Node(name='S4', index=4)
    nodes.append(node4)
    node5 = Node(name='S5', index=5)
    nodes.append(node5)

    link01 = Link(node0, node1, 500)
    links.append(link01)
    link04 = Link(node0, node4, 500)
    links.append(link04)
    link12 = Link(node1, node2, 500)
    links.append(link12)
    link14 = Link(node1, node4, 500)
    links.append(link14)
    link23 = Link(node2, node3, 500)
    links.append(link23)
    link34 = Link(node3, node4, 500)
    links.append(link34)
    link35 = Link(node3, node5, 500)
    links.append(link35)
    link45 = Link(node4, node5, 500)
    links.append(link45)

    network = Graph(links=links, nodes=nodes)
    network.printCostMatrix()

    routingModel = BinPackingRouting(network)

    flow05 = Flow(node0, node5, 200)
    flow13 = Flow(node1, node3, 50)
    flow25 = Flow(node2, node5, 100)

    # custo = 1 / capacidade_atual
    min_cost_path = network.getMinimumCostPath(flow25)
    min_cost_path = network.getMinimumCostPath(flow13)

    # flows = []
    # flows.append(flow05)
    # flows.append(flow13)
    # flows.append(flow25)
    #
    # paths = routingModel.findPaths(flows)
