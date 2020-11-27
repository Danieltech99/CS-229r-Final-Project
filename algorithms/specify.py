import copy

# Currently only supports undirected
# ... but can easly extend to directed

class SpecifySmallStep():
    def __init__(self, g, fiedler_check):
        self.graph = g
        self.fiedler_check = fiedler_check

    def is_valid_edge(self, f, target, current, bound,allow_disconnected):
        if not allow_disconnected and f == 0:
            return False
        if bound == "one" and f < target: 
            return False
        if abs(current - target) < abs(f - target):
            return False
        return True

    def fiedler_without_edge(self, g, u, v):
        g = copy.deepcopy(g)
        g[u][v] = 0
        g[v][u] = 0
        return self.fiedler_check(g), g

    def find_min_edge(self, g, target, current, bound, allow_disconnected):
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
        # print("paramaters: target {} current {} bound {} ad {}".format(target, current, bound, allow_disconnected) )
        # print("in range", list(map(lambda a: a[0], in_range)))
        res = sorted(in_range, key=lambda tup: tup[0])
        if len(res) == 0: return None
        # assert sorted in correct order
        if len(res) > 1:
            assert(res[0][0] <= res[1][0])
        return res[0]

    def cut_edges(self, target, bound = "two", allow_disconnected = False):
        g = copy.deepcopy(self.graph)
        fiedler = self.fiedler_check(g)
        i = 0

        while fiedler > target and fiedler > 0 and i < 12:
            # print("fiedler ", fiedler)
            res = self.find_min_edge(g, target, fiedler, bound, allow_disconnected)
            if res is None:
                # print("quit")
                return fiedler, g
            f, g_next = res
            fiedler = f
            g = g_next
            i += 1

        return fiedler, g

    def create_graph(self, target, bound = "two", allow_disconnected = False):
        assert(bound == "two" or bound == "one")
        _, g = self.cut_edges(target, bound, allow_disconnected)
        return g