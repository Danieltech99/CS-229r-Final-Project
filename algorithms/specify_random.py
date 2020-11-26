import copy
from random import randint, choice
from helpers.fiedler import normalized_fiedler
from algorithms.specify import SpecifySmallStep

# Currently only supports undirected
# ... but can easly extend to directed

class SpecifyRandom(SpecifySmallStep):

    def cut_edges(self, target, epsilon, bound = "two", allow_disconnected = False):
        g = copy.deepcopy(self.graph)
        l = len(g)
        edges = [(u,v) for u in range(l) for v in range(u + 1, l) if g[u][v]]

        fiedler = normalized_fiedler(g)

        while fiedler > target and fiedler > 0:

            edges_considering = copy.deepcopy(edges)
            while len(edges_considering):
                u,v = choice(edges_considering)
                f, g_next = self.fiedler_without_edge(g,u,v)
                # Invalid step
                if not allow_disconnected and f == 0:
                    continue
                # Terminal Cases
                if bound == "two" and abs(f - target) <= epsilon:
                    return f, g_next
                elif f - target <= epsilon and f - target >= 0:
                    return f, g_next
                # Valid step
                if f- target > 0:
                    fiedler = f
                    g = g_next
                    edges.remove((u,v))
                    break
                
                edges_considering.remove((u,v))
            
            if not len(edges_considering):
                return fiedler, g

        print("reached?", )
        return fiedler, g

    def create_graph(self, target, epsilon, bound = "two", allow_disconnected = False):
        assert(bound == "two" or bound == "one")
        _, g = self.cut_edges(target, epsilon, bound, allow_disconnected)
        return g