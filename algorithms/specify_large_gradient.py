import copy
from algorithms.specify_small_gradient import SpecifySmallGradient
from helpers.fiedler import leverage_score,fiedler_vector
# from helpers.get_edges import get_edges

# Currently only supports undirected
# ... but can easly extend to directed

class SpecifyLargeGradient(SpecifySmallGradient):

    def is_valid_edge(self, f, target, current, bound,allow_disconnected):
        if not allow_disconnected and f <= 0.001:
            return False
        if bound == "one" and f < target: 
            return False
        if abs(current - target) < abs(f - target):
            return False
        return True

    def gradient(self,g,u,v):
        # (vi - vj)^2
        fv = fiedler_vector(g)
        return (fv[u] - fv[v])**2

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
                res = (res[0],res[1],(u,v))
                options.append(res)
        in_range = list(filter(lambda item: self.is_valid_edge(item[0], target, current, bound,allow_disconnected), options))
        in_range = [(f, g, self.gradient(g,u,v)) for (f, g, (u,v)) in in_range]
        # Take the edge that brings us closest to the target Fiedler value
        # Thus taking the edge that changes the fiedler the "most" but not "too much"
        res = max(in_range, key=lambda tup: tup[2], default=None)
        if res is None: return None
        return res[0], res[1]

    def cut_edges(self, target, bound = "two", allow_disconnected = False):
        g = copy.deepcopy(self.graph)
        fiedler = self.fiedler_check(g)

        # Once the following constraints are violated, removing any edge is detrimental
        while fiedler > target and fiedler > 0:
            # print("fiedler ", fiedler)
            res = self.find_max_edge(g, target, fiedler, bound, allow_disconnected)
            if res is None:
                break
            f, g_next = res
            fiedler = f
            g = g_next

        return fiedler, g

    def create_graph(self, target, bound = "two", allow_disconnected = False):
        assert(bound == "two" or bound == "one")
        _, g = self.cut_edges(target, bound, allow_disconnected)
        return g