import sys
from time import time


terminal = 0
def done():
    global terminal
    terminal += 1
    # print("Reached Base Case {}".format(i))


class SpecifyDecisionTree():
    def __init__(self, g, fiedler_check, target, bound, allow_disconnected = False):
        assert(bound == "two" or bound == "one")

        self.graph = g
        self.fiedler_check = fiedler_check

        self.target = target
        self.bound = bound
        self.allow_disconnected = allow_disconnected

        # edges prevent the need to do n^2 on sparse graphs
        l = len(self.graph)
        edges = set([(u,v) for u in range(l) for v in range(u + 1, l) if self.graph[u][v]])
        self.edge_map = {}
        for i in range(len(edges) + 1):
            self.edge_map[i] = []

        t0 = time()
        self.options = self.generate_graphs(g, edges, target, bound, allow_disconnected, True)
        t1 = time()
        print("generating decision tree with {} leaves and {} options and min {} - took {}s".format(terminal, len(self.options), min((d[0] for d in self.options), default="EMPTY"), t1-t0))

    def fiedler_without_edge(self, g, u, v):
        g = g.copy()
        g[u][v] = 0
        g[v][u] = 0
        return self.fiedler_check(g), g

    def possibilities(self):
        return set(f for (f, g) in self.options)

    def search(self, data, val):
        if self.bound == "one":
            data = [x for x in data if x[0] >= val - 0.00001]
        distance = [(abs(val - f),g) for (f, g) in data]
        return min(distance, key = lambda t: t[0])

    def generate_graphs(self, g, edges, target, bound, allow_disconnected, init = False):
        if init: print("generating decision tree map")
        if edges in self.edge_map[len(edges)]: # already_explored
            return []
        else:
            self.edge_map[len(edges)].append(edges)
        
        # Base Case: Stop tree after dropped
        fiedler = self.fiedler_check(g)
        if (not allow_disconnected) and (fiedler <= 0.001):
            done()
            return []
        elif (fiedler <= 0.0001):
            done()
            return [(fiedler, g)]
        elif bound == "one" and fiedler < target: 
            # print("bounded stop")
            done()
            return []

        # Recursive Case
        options = [(fiedler, g)]
        for (u,v) in edges:
            f_modified, g_modified = self.fiedler_without_edge(g, u, v)
            # Remove edge from edge list
            edges_modified = set([edge for edge in edges if edge != (u,v)])
            assert(len(edges_modified) + 1 == len(edges))
            options += self.generate_graphs(g_modified, edges_modified, target, bound, allow_disconnected)
        return options

    def create_graph(self, target):
        fiedler = self.fiedler_check(self.graph)
        if (not self.allow_disconnected and (fiedler <= 0.0001)) or (self.bound == "one" and fiedler <= target):
            return self.graph
        
        _, g = self.search(self.options, target)
        return g