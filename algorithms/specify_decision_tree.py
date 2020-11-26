import sys
from helpers.fiedler import normalized_fiedler

i = 0
def done():
    global i
    i += 1
    print("Reached Base Case {}".format(i))

def BFS(graph): 
    s = 0
    l = len(graph)
  
    # Mark all the vertices as not visited 
    visited = [False] * (l) 

    # Create a queue for BFS 
    queue = [] 

    # Mark the source node as  
    # visited and enqueue it 
    queue.append(s) 
    visited[s] = True

    while queue: 

        # Dequeue a vertex from  
        # queue and print it 
        s = queue.pop(0) 
        print (s, end = " ") 

        # Get all adjacent vertices of the 
        # dequeued vertex s. If a adjacent 
        # has not been visited, then mark it 
        # visited and enqueue it 
        for i in range(l): 
            if graph[s][i] and visited[i] == False: 
                queue.append(i) 
                visited[i] = True
    return visited

def is_connected(graph):
    return all(BFS(graph))

class SpecifyDecisionTree():
    def __init__(self, g):
        self.graph = g

    def fiedler_without_edge(self, g, u, v):
        g = g.copy()
        g[u][v] = 0
        g[v][u] = 0
        return normalized_fiedler(g), g

    def search(self, data, val):
        # found = sorted(data, key=lambda tup: tup[0])[0]
        # b = BFS(found[1])
        # print("options to search", len(data), min([d[0] for d in data]), min([d[0] for d in data]) == 0, found[0], all(b), b, "\n",found[1])
        selected = (sys.maxsize, None)
        for item in data:
            if abs(selected[0] - val) >= abs(item[0] - val):
                selected = item
        return selected

    def generate_graphs(self, g, edges, target, bound, allow_disconnected):
        if edges in self.edge_map[len(edges)]: # already_explored
            return []
        else:
            self.edge_map[len(edges)].append(edges)
        
        # Base Case: Stop tree after dropped
        fiedler = normalized_fiedler(g)
        if not allow_disconnected and (fiedler <= 0.0001):
            # done()
            return []
        elif bound == "one" and fiedler <= target: 
            # done()
            return [(fiedler, g)]
        elif (fiedler <= 0.0001):
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
        # [lowClosest, highClosest] = self.search(graphs, target)
        # if lowClosest != highClosest:
        #     print("\t Found Two: {} and {}".format(graphs[lowClosest][0], graphs[highClosest][0]))
        return self.search(graphs, target)

    def create_graph(self, target, bound = "two", allow_disconnected = False):
        assert(bound == "two" or bound == "one")

        fiedler = normalized_fiedler(self.graph)
        if not allow_disconnected and (fiedler <= 0.0001):
            return self.graph

        # edges prevent the need to do n^2 on sparse graphs
        l = len(self.graph)
        edges = set([(u,v) for u in range(l) for v in range(u + 1, l) if self.graph[u][v]])
        _, g = self.find_graph(self.graph, edges, target, bound, allow_disconnected)
        return g