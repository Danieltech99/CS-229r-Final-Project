from helpers.fiedler import normalized_fiedler

i = 0
def done():
    global i
    i += 1
    print("Reached Base Case {}".format(i))

class SpecifyDecisionTree():
    def __init__(self, g):
        self.graph = g

    def fiedler_without_edge(self, g, u, v):
        g = g.copy()
        g[u][v] = 0
        g[v][u] = 0
        return normalized_fiedler(g), g

    def binarySearch(self, data, val):
        highIndex = len(data)-1
        lowIndex = 0
        while highIndex > lowIndex:
            index = (highIndex + lowIndex) // 2
            sub = data[index][0]
            if data[lowIndex][0] == val:
                return [lowIndex, lowIndex]
            elif sub == val:
                return [index, index]
            elif data[highIndex][0] == val:
                return [highIndex, highIndex]
            elif sub > val:
                if highIndex == index:
                    return sorted([highIndex, lowIndex])
                highIndex = index
            else:
                if lowIndex == index:
                    return sorted([highIndex, lowIndex])
                lowIndex = index
        return sorted([highIndex, lowIndex])

    def generate_graphs(self, g, edges, target, bound, allow_disconnected):
        if edges in self.edge_map[len(edges)]: # already_explored
            return []
        else:
            self.edge_map[len(edges)].append(edges)
        
        # Base Case: Stop tree after dropped
        fiedler = normalized_fiedler(g)
        if not allow_disconnected and fiedler == 0:
            # done()
            return []
        elif bound == "one" and fiedler <= target: 
            # done()
            return [(fiedler, g)]
        elif len(edges) == 0:
            # done()
            return [(fiedler, g)]

        # Recursive Case
        options = [(fiedler, g)]
        for (u,v) in edges:
            f_modified, g_modified = self.fiedler_without_edge(g, u, v)
            # Remove edge from edge list
            edges_modified = set([edge for edge in edges if edge != (u,v)])
            assert(len(edges_modified) + 1 == len(edges))
            options += self.generate_graphs(g_modified, edges_modified, target, bound, allow_disconnected)
        return options

    def find_graph(self, g, edges, target, bound, allow_disconnected):
        self.edge_map = {}
        for i in range(len(edges) + 1):
            self.edge_map[i] = []
        graphs = self.generate_graphs(g, edges, target, bound, allow_disconnected)
        [lowClosest, highClosest] = self.binarySearch(graphs, target)
        if lowClosest != highClosest:
            print("\t Found Two: {} and {}".format(graphs[lowClosest][0], graphs[highClosest][0]))
        return graphs[highClosest]

    def create_graph(self, target, bound = "two", allow_disconnected = False):
        assert(bound == "two" or bound == "one")

        fiedler = normalized_fiedler(self.graph)
        if not allow_disconnected and fiedler == 0:
            return self.graph

        # edges prevent the need to do n^2 on sparse graphs
        l = len(self.graph)
        edges = set([(u,v) for u in range(l) for v in range(u + 1, l) if self.graph[u][v]])
        _, g = self.find_graph(self.graph, edges, target, bound, allow_disconnected)
        return g