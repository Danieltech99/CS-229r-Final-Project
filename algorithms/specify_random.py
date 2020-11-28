import copy
from random import randint, choice
from algorithms.specify import SpecifySmallStep
from helpers.fiedler import fiedler as calc_fielder

# Currently only supports undirected
# ... but can easly extend to directed

class SpecifyRandom(SpecifySmallStep):

    def cut_edges(self, target, bound, allow_disconnected):
        g = copy.deepcopy(self.graph)
        l = len(g)
        edges = [(u,v) for u in range(l) for v in range(u + 1, l) if g[u][v]]

        fiedler = self.fiedler_check(g)

        while fiedler > target and fiedler > 0:

            edges_considering = copy.deepcopy(edges)
            while len(edges_considering):
                u,v = choice(edges_considering)
                f, g_next = self.fiedler_without_edge(g,u,v)
                # Invalid step
                if (not allow_disconnected) and self.fiedler_check(g_next) < 0.0001:
                    edges_considering.remove((u,v))
                    continue
                # Terminal Cases
                if bound == "two" and abs(f - target) > abs(fiedler - target):
                    edges_considering.remove((u,v))
                    continue
                elif bound == "one" and f < target:
                    edges_considering.remove((u,v))
                    continue
                fiedler = f
                g = g_next
                edges.remove((u,v))
                break
                
                
            
            if not len(edges_considering):
                return fiedler, g

        return fiedler, g

    def create_graph(self, target, bound = "two", allow_disconnected = False, runs = 10):
        assert(bound == "two" or bound == "one")
        
        graphs = [self.cut_edges(target, bound, allow_disconnected) for i in range(runs)]
        distance = [(abs(target - f),g) for (f, g) in graphs]
        return min(distance, key = lambda t: t[0])[1]