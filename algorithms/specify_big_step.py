import copy
from algorithms.specify import SpecifySmallStep
from helpers.get_edges import get_edges

# Currently only supports undirected
# ... but can easly extend to directed

class SpecifyBigStep(SpecifySmallStep):

    def is_valid_edge(self, f, target, current, bound,allow_disconnected):
        if not allow_disconnected and f == 0:
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
        sorted_greatest = list(sorted(in_range, key=lambda tup: tup[0], reverse=True))
        # assert sorted in correct order
        if len(sorted_greatest) > 1:
            assert(sorted_greatest[0][0] >= sorted_greatest[1][0])
        return sorted_greatest and sorted_greatest[0]

    def cut_edges(self, target, bound = "two", allow_disconnected = False):
        g = copy.deepcopy(self.graph)
        fiedler = self.fiedler_check(g)

        while fiedler > target and fiedler > 0:
            res = self.find_max_edge(g, target, fiedler, bound, allow_disconnected)
            # print("recivef cut", res)
            if res == []:
                # print("quit")
                return fiedler, g
            f, g_next = res
            # if f == fiedler:
            #     print("\tfound a fielder match\n",f, get_edges(g_next), "\n",fiedler, get_edges(g))
            assert(f <= fiedler)
            fiedler = f
            g = g_next

        return fiedler, g

    def create_graph(self, target, bound = "two", allow_disconnected = False):
        assert(bound == "two" or bound == "one")
        _, g = self.cut_edges(target, bound, allow_disconnected)
        return g