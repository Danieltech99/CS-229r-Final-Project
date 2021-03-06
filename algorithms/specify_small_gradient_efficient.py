import copy
from algorithms.specify import SpecifySmallStep
from helpers.fiedler import leverage_score,fiedler_vector
from algorithms.specify_small_gradient import SpecifySmallGradient
# from helpers.get_edges import get_edges

# Currently only supports undirected
# ... but can easly extend to directed

class SpecifySmallGradientEfficient(SpecifySmallGradient):

    def is_valid_edge(self, f, target, current, bound,allow_disconnected):
        if not allow_disconnected and f <= 0.001:
            return False
        if bound == "one" and f < target: 
            return False
        if abs(current - target) < abs(f - target):
            return False
        return True

    # Try removing all edges that dont influence the fiedler value
    def remove_all_non_contributing_edges(self, g):
        f = self.fiedler_check(g)
        for u in range(len(g)):
            for v in range(u):
                res = self.fiedler_without_edge(g,u,v)
                if res[0] == f:
                    g = res[1]
                    print("removing")
        f_new = self.fiedler_check(g)
        print("f_old {} and f_new {}".format(f, f_new))
        assert(f_new < f + 0.001 and f_new > f - 0.001)
        return g

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
        grad = self.gradient(g)
        in_range = [(f, g_p, grad((u,v))) for (f, g_p, (u,v)) in in_range]
        # Take the edge that brings us closest to the target Fiedler value
        # Thus taking the edge that changes the fiedler the "most" but not "too much"
        res = min(in_range, key=lambda tup: tup[2], default=None)
        if res is None: return None
        return res[0], res[1]

    def cut_edges(self, target, bound = "two", allow_disconnected = False):
        g = copy.deepcopy(self.graph)
        fiedler = self.fiedler_check(g)

        # Once the following constraints are violated, removing any edge is detrimental
        while fiedler > target and fiedler > 0:
            # print("fiedler ", fiedler)
            g = self.remove_all_non_contributing_edges(g)
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