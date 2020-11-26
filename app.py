import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
import argparse
from consensus import Graph, Node
from helpers.fiedler import fiedler, normalized_fiedler
from formations import formations
from algorithms.prims import Graph as PrimGraph
from algorithms.specify import SpecifySmallStep
from algorithms.specify_big_step import SpecifyBigStep
from algorithms.specify_random import SpecifyRandom
from algorithms.specify_decision_tree import SpecifyDecisionTree



class Test(ABC):
    @abstractmethod
    def create_graph(self):
        pass

class TestFull(Test):
    name = "Full"
    target_connectivity = "N/A"
    bound = "N/A"
    def create_graph(self, formation):
        g = Graph(formation["nodes"], formation["full"])
        # name = "{} on {} - Fiedler {} - Norm Fiedler {}".format(formation["name"], self.name, fiedler(g.adj_matrix), normalized_fiedler(g.adj_matrix))
        # print(name)
        return g

class TestSpecifyDecisionTree(Test):
    # name_base = "Specify (Decision Tree)"
    name_base = "Decision Tree"
    name = "Decision Tree"
    def __init__(self, target_connectivity, bound = "two"):
        self.target_connectivity = target_connectivity
        self.bound = bound
        # self.name = "{} c={} bound={}".format(self.name_base, self.target_connectivity, bound)
    def create_graph(self, formation):
        g = SpecifyDecisionTree(formation["full"]).create_graph(self.target_connectivity, self.bound)
        return Graph(formation["nodes"], g)

class TestSpecifySmallStep(Test):
    # name_base = "Specify (Small Step)"
    name_base = "Small Step"
    name = "Small Step"
    def __init__(self, target_connectivity, bound = "two"):
        self.target_connectivity = target_connectivity
        self.bound = bound
        # self.name = "{} c={} bound={}".format(self.name_base, self.target_connectivity, bound)
    def create_graph(self, formation):
        g = SpecifySmallStep(formation["full"]).create_graph(self.target_connectivity, self.bound)
        return Graph(formation["nodes"], g)

class TestSpecifyBigStep(Test):
    # name_base = "Specify (Big Step)"
    name_base = "Big Step"
    name = "Big Step"
    def __init__(self, target_connectivity, bound = "two"):
        self.target_connectivity = target_connectivity
        self.bound = bound
        # self.name = "{} c={} bound={}".format(self.name_base, self.target_connectivity, bound)
    def create_graph(self, formation):
        g = SpecifyBigStep(formation["full"]).create_graph(self.target_connectivity, self.bound)
        return Graph(formation["nodes"], g)

class TestSpecifyRandom(Test):
    # name_base = "Specify (Random)"
    name_base = "Random"
    name = "Random"
    def __init__(self, target_connectivity, epsilon, bound = "two"):
        self.target_connectivity = target_connectivity
        self.bound = bound
        self.epsilon = epsilon
        # self.name = "{} c={} epsilon={} bound={}".format(self.name_base, self.target_connectivity, epsilon, bound)
    def create_graph(self, formation):
        g = SpecifyRandom(formation["full"]).create_graph(self.target_connectivity, self.epsilon, self.bound)
        return Graph(formation["nodes"], g)

if __name__ == "__main__":

    # To Create a New Test
    # ... create a class with a `create_graph` method and a name property
    # ... that takes in a formation and outputs a Graph object
    # Then add Test Class to Array
    # ... each test will be supplied a formation based on the args
    tests = [TestFull()]
    paramter_trials = [0.25, 0.5, 0.75, 1, 1.25]
    test_types = []
    test_types = [lambda t: TestSpecifyDecisionTree(t),
        lambda t: TestSpecifySmallStep(t),
        lambda t: TestSpecifyBigStep(t),
        lambda t: TestSpecifySmallStep(t, "one"),
        lambda t: TestSpecifyBigStep(t, "one")
        ]
    for t in paramter_trials:
        tests += [t_f(t) for t_f in test_types]
    # tests += [TestSpecifyDecisionTree(t) for t in paramter_trials]
    # tests += [TestSpecifySmallStep(t) for t in paramter_trials]
    # tests += [TestSpecifySmallStep(t, "one") for t in paramter_trials]
    # tests += [TestSpecifyBigStep(t) for t in paramter_trials]
    # tests += [TestSpecifyBigStep(t, "one") for t in paramter_trials]


    # tests += [TestSpecifyRandom(t, 0.2) for t in paramter_trials]
    # tests += [TestSpecifyRandom(t, 0.2, "one") for t in paramter_trials]
    # tests += [TestSpecifyRandom(t, 0.1) for t in paramter_trials]
    # tests += [TestSpecifyRandom(t, 0.1, "one") for t in paramter_trials]

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=int, help="enter a test number/id",
                        nargs='?', default=0, const=0, choices=range(0, len(tests) + 1))
    parser.add_argument("--formation", type=int, help="enter a formation number/id",
                        nargs='?', default=1, const=0, choices=range(0, len(formations) + 1))
    args = parser.parse_args()

    # To Create a Formation, add one to `formations.py`
    if args.formation == 0:
        forms = formations
    else: 
        form = formations[args.formation - 1]
        forms = [form]

    dash = '-' * 40
    columns = ["Formation", "Algorithm", "Target λ", "Side", "Result λ", "Result ν"]
    print(dash)
    print('{:<10s}{:<16s}{:<12s}{:<8s}{:<10s}{:<10s}'.format(*columns))
    print(dash)
    
    for formation in forms:
        print()
        for x in paramter_trials:
            for t_f in test_types:
                test = t_f(x)
                (test,graph) = (test, test.create_graph(formation))

                # Better print formatting 
                # https://scientificallysound.org/2016/10/17/python-print3/
                print('{:<10s}{:<16s}{:<12s}{:<8s}{:<10.4f}{:<10.4f}'.format(formation["name"], test.name, str(test.target_connectivity), test.bound, fiedler(graph.adj_matrix), normalized_fiedler(graph.adj_matrix)))
                # name = "{} on {} - Fiedler {} - Norm Fiedler {}".format(formation["name"], test.name, fiedler(graph.adj_matrix), normalized_fiedler(graph.adj_matrix))
                # print(name)
            print()