from .link import Link
from .node import Node

INVALID_VALUE = -1

## Considera Node como string (id do switch)
class Graph(object):
    def __init__(self, links = [], nodes = []):
        self.cost = {}
        self.links = links
        self.nodes = nodes

        self.createCostMatrix()

    def addLink(self, node_id_1, node_id_2, weight):
        link = Link(node_id_1, node_id_2, weight)
        self.links.append(link)

        # TODO: Como saber a capacidade do link? Por enquanto, está fixa no código.
        # print('node1.id = ', node1.id)
        # print('node2.id = ', node2.id)
        #
        # print('link.node1.id = ', link.node1.id)
        # print('link.node2.id = ', link.node2.id)
        # print('link.weight = ', link.weight)
        #
        # print('cost matrix = ', self.cost)
        # print('cost matrix[link.node1.id] = ', self.cost[link.node1.id])
        # print('cost matrix[link.node2.id] = ', self.cost[link.node2.id])

        self.cost[link.node1][link.node2] = 1/link.weight
        self.cost[link.node2][link.node1] = 1/link.weight

    def containsLink(self, node_id_1, node_id_2):
        for link in self.links:
            if (link.node1 == node_id_1 and link.node2 == node_id_2) or (link.node1 == node_id_2 and link.node2 == node_id_1):
                return True
        return False

    def removeLink(self, node_id_1, node_id_2):
        for link in self.links:
            if (link.node1 == node_id_1 and link.node2 == node_id_2) or (link.node1 == node_id_2 and link.node2 == node_id_1):
                link_index = self.links.index(link)
                del self.links[link_index]

                # TODO: Remover da matriz de adjacencia  === Colocar valor inválido
                self.cost[link.node1][link.node2] = INVALID_VALUE
                self.cost[link.node2][link.node1] = INVALID_VALUE

    def addNode(self, node_id):
        self.nodes.append(node_id)
        self.cost[node_id] = {}

    def removeNode(self, node_id):
        for node in self.nodes:
            if node == node_id:
                node_index = self.nodes.index(node)
                del self.nodes[node_index]

                # TODO: Remover da matriz de adjacencia tb

    def containsNodeId(self, node_id):
        for node in self.nodes:
            if node == node_id:
                return True
        return False

    def createCostMatrix(self):
        if len(self.links) == 0: return

        # cost is NxN array of 'foo' (which can depend on i and j if you want)
        self.cost = [[float('inf') for i in range(len(self.nodes))] for j in range(len(self.nodes))]

        for link in self.links:
            # Inicializa custo bidirecional
            self.cost[link.node1][link.node2] = 1 / link.weight
            self.cost[link.node2][link.node1] = 1 / link.weight

    def createDistancesDict(self):
        # Cria dicionário de distâncias de cada nodo até todos os outros
        # distances = {
        #     'B': {'A': 5, 'D': 1, 'G': 2},
        #     'A': {'B': 5, 'D': 3, 'E': 12, 'F' :5},
        #     'D': {'B': 1, 'G': 1, 'E': 1, 'A': 3},
        #     'G': {'B': 2, 'D': 1, 'C': 2},
        #     'C': {'G': 2, 'E': 1, 'F': 16},
        #     'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
        #     'F': {'A': 5, 'E': 2, 'C': 16}}
        print('self.cost = {0}'.format(self.cost))
        distances = {}
        for node1 in self.nodes:
            # Percorre a linha
            distances[node1] = {}
            for node2 in self.nodes:
                print('distances[{0}] = {1}'.format(node1, self.cost[node1]))

                distances[node1][node2] = self.cost[node1][node2]

        return distances

    def updatePathCostMatrix(self, path, consumed_bandwidth):
        # Atualiza as larguras de banda disponiveis de cada link
        for i in range(len(path) - 1):
            item_index_source = path[i]
            item_index_target = path[i+1]
            self.cost[item_index_source][item_index_target] = self.cost[item_index_source][item_index_target] - (1 / consumed_bandwidth)

        new_distances = self.createDistancesDict()

        print(' - Updated cost')
        self.printCostMatrix()
        print('\n\n')


    def getMinimumCostPath(self, flow):
        # Calcula caminho de custo mínimo, onde o custo de cada caminho é o recíproco
        # da sua capacidade disponível (1/capacidade). Após associar um par de
        # switches a um caminho, atualiza o custo de cada link.
        print('-> Get mininum cost path [Dijkstra] from {0} to {1}\n'.format(
            flow.source, flow.target))

        min_cost_path = self.dijsktra(flow.source, flow.target)
        print(' - Path found: {0}\n'.format(min_cost_path))

        self.updatePathCostMatrix(min_cost_path, flow.bandwidth)

        return min_cost_path

    def dijsktra(self, source, target):
        # shortest paths is a dict of nodes whose value is a tuple of (previous node, weight)
        shortest_paths = {source: (None, 0)}
        current_node = source
        distances = self.createDistancesDict()
        visited = set()

        while current_node != target:
            visited.add(current_node)
            destinations = distances[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = self.cost[current_node][next_node] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}

            if len(next_destinations.values()) == 0:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        return path

    def printCostMatrix(self):
        print('-> Cost matrix:')
        print(self.cost)
        print('\n')

    def printGraph(self):
        for link in self.links:
            print('{node1}-------({weight})-------{node2}'.format(
                node1=link.node1,
                weight=link.weight,
                node2=link.node2
            ))
