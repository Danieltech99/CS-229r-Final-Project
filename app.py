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
from helpers.get_edges import get_edges
from collections import OrderedDict 


class Test(ABC):
    @abstractmethod
    def create_graph(self):
        pass

# class Full():
#     def __init__(self, g, target_connectivity, bound):
#         self.g = g
#     def create_graph(self, target_connectivity):
#         return self.g
class TestFull(Test):
    name = "Full"
    target_connectivity = "N/A"
    bound = "N/A"
    def __init__(self, formation):
        # self.target_connectivity = target_connectivity
        # self.bound = bound
        self.formation = formation
        # self.alg = Full(formation["full"], self.target_connectivity, self.bound) 
    def create_graph(self, target_connectivity = None):
        # g = self.alg.g
        g = self.formation["full"]
        return Graph(self.formation["nodes"], g)

class TestSpecifyDecisionTree(Test):
    name = "Decision Tree"
    def __init__(self, formation, fiedler_check, bound = "two", target_connectivity = 0):
        self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifyDecisionTree(self.formation["full"], fiedler_check, self.target_connectivity, self.bound) 
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity)
        return Graph(self.formation["nodes"], g)

class TestSpecifySmallStep(Test):
    name = "Small Step"
    def __init__(self, formation, fiedler_check, bound = "two"):
        # self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifySmallStep(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound)
        return Graph(self.formation["nodes"], g)

class TestSpecifyBigStep(Test):
    name = "Big Step"
    def __init__(self, formation, fiedler_check, bound = "two"):
        # self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifyBigStep(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound)
        return Graph(self.formation["nodes"], g)

class TestSpecifyRandom(Test):
    name = "Random"
    def __init__(self, formation, fiedler_check, bound = "two", runs = 10):
        self.bound = bound
        self.formation = formation
        # self.runs = runs
        self.runs = 10 * len(self.formation["nodes"])
        self.alg = SpecifyRandom(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound, runs=self.runs)
        return Graph(self.formation["nodes"], g)




def plot_alg(data, paramter_trials):
    print("data", data)
    for formation in forms:
        labels = paramter_trials

        x = np.arange(len(labels))  # the label locations
        width = 0.2  # the width of the bars

        fig, ax = plt.subplots()
        rects = []
        i = 0
        for name,bar_data in data.items():
            print("adding abr", name, " with data ", bar_data[formation["name"]])
            rects += [ax.bar(x + (width * i), bar_data[formation["name"]].values(), width, label=name, bottom=0)]
            i += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Achived Fiedler Value')
        ax.set_xlabel('Desired Fiedler Value')
        ax.set_title('Algorithm Comparision (Formation {})'.format(formation["name"]))
        ax.set_xticks(x + width / 2)
        ax.set_xticklabels(labels)
        # ax.legend()
        ax.legend(tuple([b[0] for b in rects]), tuple(data.keys()))
        ax.autoscale_view()

        fig.tight_layout()

    plt.show()



# Plot algorithm performance seperately
# def plot_alg(data, paramter_trials):
#     print("data", data)
#     for formation in forms:
#         for trial in paramter_trials:
#             labels = data.keys()

#             x = np.arange(len(labels))  # the label locations
#             vals = [item[formation["name"]][trial] for item in data.values()]

#             fig, ax = plt.subplots()
#             ax.bar(x, vals)

#             # Add some text for labels, title and custom x-axis tick labels, etc.
#             ax.set_ylabel('Achived Fiedler Value')
#             ax.set_xlabel('Algorithm')
#             ax.set_title('Algorithm Comparision (Desired Fiedler: {}) (Formation: {})'.format(trial, formation["name"]))
#             ax.set_xticks(x)
#             ax.set_xticklabels(labels)
#             # ax.legend()


#             # def autolabel(rects):
#             #     """Attach a text label above each bar in *rects*, displaying its height."""
#             #     for rect in rects:
#             #         height = rect.get_height()
#             #         ax.annotate('{}'.format(height),
#             #                     xy=(rect.get_x() + rect.get_width() / 2, height),
#             #                     xytext=(0, 3),  # 3 points vertical offset
#             #                     textcoords="offset points",
#             #                     ha='center', va='bottom')


#             # autolabel(rects1)
#             # autolabel(rects2)

#             fig.tight_layout()

#     plt.show()

if __name__ == "__main__":
    
    # 
    # Arguments
    # 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--formation", type=int, help="enter a formation number/id",
                        nargs='?', default=1, const=0, choices=range(0, len(formations) + 1))
    args = parser.parse_args()

    # To Create a Formation, add one to `formations.py`
    if args.formation == 0:
        forms = formations
    else: 
        form = formations[args.formation - 1]
        forms = [form]


    # To Create a New Test
    # ... create a class with a `create_graph` method and a name property
    # ... that takes in a formation and outputs a Graph object
    # Then add Test Class to Array
    # ... each test will be supplied a formation based on the args
    paramter_trials = [0.25, 0.5, 0.75, 1, 1.25]
    # paramter_trials = [0.5, 0.75]
    
 

    # 
    # Run Simulations
    # 

    dash = '-' * 40
    columns = ["Formation", "Algorithm", "Target λ", "Side", "Result λ", "Result ν", "Edges"]
    print(dash)
    print('{:<10s}{:<16s}{:<12s}{:<8s}{:<10s}{:<10s}{:<20s}'.format(*columns))
    print(dash)

    # Preload classes to allow decision tree to make only once

    results = {}
    alg_results = OrderedDict()
    for formation in forms:
        results[formation["name"]] = {}
        # alg_results[formation["name"]] = {}

        test_types = [
            # TestSpecifyDecisionTree(formation, normalized_fiedler, bound="one", target_connectivity=min(paramter_trials)),
            # TestSpecifyDecisionTree(formation),
            # TestSpecifySmallStep(formation),
            # TestSpecifyBigStep(formation),

            # TestSpecifyRandom(formation, normalized_fiedler, "one"),
            # TestSpecifySmallStep(formation, normalized_fiedler, "one"),
            # TestSpecifyBigStep(formation, normalized_fiedler, "one"),

            # # switch to regular Fiedler
            TestSpecifyDecisionTree(formation, fiedler, bound="one", target_connectivity=min(paramter_trials)),
            # TestSpecifyDecisionTree(formation, fiedler),
            # TestSpecifySmallStep(formation, fiedler),
            # TestSpecifyBigStep(formation, fiedler),
            TestSpecifyRandom(formation, fiedler, "one"),
            TestSpecifySmallStep(formation, fiedler, "one"),
            TestSpecifyBigStep(formation, fiedler, "one"),
        ]

        test = TestFull(formation)
        (test,graph) = (test, test.create_graph(None))
        nf = fiedler(graph.adj_matrix)
        results[formation["name"]]["true"] = nf
        print('{:<10s}{:<16s}{:<12s}{:<8s}{:<10.4f}{:<10.4f}{:<20s}'.format(formation["name"], test.name, str(test.target_connectivity), test.bound, fiedler(graph.adj_matrix), normalized_fiedler(graph.adj_matrix), str(get_edges(graph.adj_matrix))))
        print()
        for x in paramter_trials:
            for t_f in test_types:
                # test = t_f(x)
                test = t_f
                (test,graph) = (test, test.create_graph(x))

                # Better print formatting 
                # https://scientificallysound.org/2016/10/17/python-print3/
                tnf = fiedler(graph.adj_matrix)
                
                # test_n = "{} ({} sided)".format(test.name, test.bound)
                test_n = test.name
                if test_n not in alg_results: alg_results[test_n] = {}
                if formation["name"] not in alg_results[test_n]: alg_results[test_n][formation["name"]] = {}
                if x not in alg_results[test_n][formation["name"]]: alg_results[test_n][formation["name"]][x] = {}
                alg_results[test_n][formation["name"]][x] = tnf
                
                print('{:<10s}{:<16s}{:<12s}{:<8s}{:<10.4f}{:<10.4f}{:<20s}'.format(formation["name"], test.name, str(x), test.bound, fiedler(graph.adj_matrix), tnf, str(get_edges(graph.adj_matrix))))
            print()
    plot_alg(alg_results,paramter_trials)
    # print("test")
    # print("Norm ", normalized_fiedler(np.array([[0,0],[0,0]])))
    # print("Norm ", normalized_fiedler(np.array([[1,0],[0,1]])))