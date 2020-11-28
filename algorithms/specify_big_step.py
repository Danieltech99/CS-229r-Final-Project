import copy
from algorithms.specify import SpecifySmallStep
from helpers.get_edges import get_edges

# Currently only supports undirected
# ... but can easly extend to directed

class SpecifyBigStep(SpecifySmallStep):

    def is_valid_edge(self, f, target, current, bound,allow_disconnected):
        if not allow_disconnected and f <= 0.001:
            return False
        if bound == "one" and f < target: 
            return False
        if abs(current - target) < abs(f - target):
            return False
        return True

    def find_max_edge(self, g, target, current, bound,allow_disconnected):
        l = len(g)
        options = []
        for u in range(l):
            # want to ensure u < v
            # ... to prevent double traversing
            # Modify here to support directed graphs
            for v in range(u + 1, l):
                assert(u < v)
                if g[u][v] == 0: continue
                res = self.fiedler_without_edge(g,u,v)
                options.append(res)
        in_range = list(filter(lambda item: self.is_valid_edge(item[0], target, current, bound,allow_disconnected), options))
        in_range = [(f, g, abs(f - target)) for (f, g) in in_range]
        res = min(in_range, key=lambda tup: tup[2], default=None)
        if res is None: return None
        return res[0], res[1]

    def cut_edges(self, target, bound = "two", allow_disconnected = False):
        g = copy.deepcopy(self.graph)
        fiedler = self.fiedler_check(g)

        while fiedler > target and fiedler > 0:
            # print("fiedler ", fiedler)
            res = self.find_max_edge(g, target, fiedler, bound, allow_disconnected)
            if res is None:
                # print("quit")
                break
            f, g_next = res
            fiedler = f
            g = g_next

        return fiedler, g

    def create_graph(self, target, bound = "two", allow_disconnected = False):
        assert(bound == "two" or bound == "one")
        _, g = self.cut_edges(target, bound, allow_disconnected)
        return g