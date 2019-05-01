import time

from random import randrange
from collections import defaultdict

# Cisco Reference bandwidth = 1 Gbps
REFERENCE_BW = 10000000

FIRST_PATH = True
MIN_HOPS = False
RANDOM = False

class ControllerUtilities(object):

    def __init__(self, adjacency, datapath_list, bandwidths):
        self.adjacency = adjacency
        self.datapath_list = datapath_list         # dicionário cuja chave é o ID do switch e o valor é datapath correspondente
        self.bandwidths = bandwidths

    def getPaths(self, src, dst):
        '''
        Get all paths from src to dst using DFS algorithm
        '''
        if src == dst:
            # Significa que o host e o destino estão conectados ao mesmo switch.
            return [[src]]

        paths = []
        stack = [(src, [src])]

        while stack:
            (node, path) = stack.pop()
            for next in set(self.adjacency[node].keys()) - set(path):
                if next is dst:
                    paths.append(path + [next])
                else:
                    stack.append((next, path + [next]))

        print("Caminhos disponiveis de {0} para {1}: {2}".format(src, dst, paths))
        return paths

    def getLinkCost(self, s1, s2):
        '''
        Get the link cost between two switches
        '''
        e1 = self.adjacency[s1][s2]
        e2 = self.adjacency[s2][s1]
        bl = min(self.bandwidths[s1][e1], self.bandwidths[s2][e2])
        ew = REFERENCE_BW/bl
        return ew

    def getPathCost(self, path):
        '''
        Get the path cost
        '''
        cost = 0
        for i in range(len(path) - 1):
            cost += self.getLinkCost(path[i], path[i+1])
        return cost


    def addPortsToPath(self, paths, first_port, last_port):
        '''
        Add the ports that connects the switches for all paths
        '''
        paths_p = []
        for path in paths:
            p = {}
            in_port = first_port
            for s1, s2 in zip(path[:-1], path[1:]):
                out_port = self.adjacency[s1][s2]
                p[s1] = (in_port, out_port)
                in_port = self.adjacency[s2][s1]
            p[path[-1]] = (in_port, last_port)
            paths_p.append(p)

        return paths_p[0]

    def getFirstPath(self, paths):
        return paths[0]

    def getMinimumHopsPath(self, paths):
        # retorna o primeiro caminho com o número mínimo de hops
        paths_cost = []

        for path in paths:
            paths_cost.append(self.getPathCost(path))

        index_min = paths_cost.index(min(paths_cost))

        return paths[index_min]

    def getRandomPath(self, paths):
        index = randrange(len(paths))
        return paths[index]

    def choosePathAccordingToHeuristic(self, src, dst):
        paths = self.getPaths(src, dst)

        # De acordo com a heuristica escolhida:
        final_path = []

        if FIRST_PATH:
            final_path = self.getFirstPath(paths)
        elif MIN_HOPS:
            final_path = self.getMinimumHopsPath(paths)
        elif RANDOM:
            final_path = self.getRandomPath(paths)
        else:
            print('Erro: heuristica nao escolhida. Retornou caminho vazio')

        print('Caminho escolhido = {0}'.format(final_path))
        return final_path
