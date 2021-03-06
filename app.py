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
from algorithms.specify_small_resistance import SpecifySmallLeverage
from algorithms.specify_large_resistance import SpecifyLargeLeverage
from algorithms.specify_small_gradient import SpecifySmallGradient
from algorithms.specify_small_gradient_efficient import SpecifySmallGradientEfficient
from algorithms.specify_large_gradient import SpecifyLargeGradient
from algorithms.specify_random import SpecifyRandom
from algorithms.specify_decision_tree import SpecifyDecisionTree
from helpers.get_edges import get_edges
from collections import OrderedDict 
from helpers.mkdir_p import mkdir_p


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
    color = "slategray"
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
    color = "black"
    def __init__(self, formation, fiedler_check, bound = "two", target_connectivity = 0):
        self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifyDecisionTree(self.formation["full"], fiedler_check, self.target_connectivity, self.bound) 
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity)
        return Graph(self.formation["nodes"], g)

class TestSpecifySmallStep(Test):
    name = "Small Cut"
    color = "tab:blue"
    def __init__(self, formation, fiedler_check, bound = "two"):
        # self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifySmallStep(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound)
        return Graph(self.formation["nodes"], g)

class TestSpecifyBigStep(Test):
    name = "Big Cut"
    color = "tab:orange"
    def __init__(self, formation, fiedler_check, bound = "two"):
        # self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifyBigStep(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound)
        return Graph(self.formation["nodes"], g)

class TestSpecifySmallLeverage(Test):
    name = "Small Leverage"
    color = "limegreen"
    def __init__(self, formation, fiedler_check, bound = "two"):
        # self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifySmallLeverage(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound)
        return Graph(self.formation["nodes"], g)

class TestSpecifyLargeLeverage(Test):
    name = "Big Leverage"
    color = "forestgreen"
    def __init__(self, formation, fiedler_check, bound = "two"):
        # self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifyLargeLeverage(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound)
        return Graph(self.formation["nodes"], g)


class TestSpecifySmallGradient(Test):
    name = "Small Gradient"
    color = "tab:pink"
    def __init__(self, formation, fiedler_check, bound = "two"):
        # self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifySmallGradient(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound)
        return Graph(self.formation["nodes"], g)

class TestSpecifySmallGradientEfficient(Test):
    color = "tab:brown"
    name = "Small Gradient Efficient"
    def __init__(self, formation, fiedler_check, bound = "two"):
        # self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifySmallGradientEfficient(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound)
        return Graph(self.formation["nodes"], g)

class TestSpecifyLargeGradient(Test):
    name = "Big Gradient"
    color = "tab:purple"
    def __init__(self, formation, fiedler_check, bound = "two"):
        # self.target_connectivity = target_connectivity
        self.bound = bound
        self.formation = formation
        self.alg = SpecifyLargeGradient(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound)
        return Graph(self.formation["nodes"], g)

class TestSpecifyRandom(Test):
    name = "Random"
    color = "tab:red"
    def __init__(self, formation, fiedler_check, bound = "two", runs = 3):
        self.bound = bound
        self.formation = formation
        # self.runs = runs
        self.runs = runs * len(self.formation["nodes"])
        self.alg = SpecifyRandom(self.formation["full"], fiedler_check)
    def create_graph(self, target_connectivity):
        g = self.alg.create_graph(target_connectivity, self.bound, runs=self.runs)
        return Graph(self.formation["nodes"], g)




def plot_bar_alg(data, parameter_trials, formation, save_path = "compare_algorithms"):
    labels = parameter_trials

    x = np.arange(len(labels))  # the label locations
    width = 0.10  # the width of the bars

    fig, ax = plt.subplots(figsize=(10,10))
    rects = []
    i = 0
    for (name, color),bar_data in data.items():
        rects += [ax.bar(x + (width * i), bar_data.values(), width, label=name, bottom=0, color=color)]
        i += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Achived Fiedler Value')
    ax.set_xlabel('Desired Fiedler Value')
    ax.set_title('Algorithm Comparision (Formation {})'.format(formation["name"]))
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(labels)
    # ax.legend()
    ax.legend(tuple([b[0] for b in rects]), tuple(name for (name,_) in data.keys()))
    ax.autoscale_view()

    fig.tight_layout()

    save_name = formation["name"]
    mkdir_p("figures/{}".format(save_path))
    if save_name: 
        plt.savefig("figures/{}/{}.png".format(save_path,save_name))
        plt.close()

    plt.show()


def random_graph(size, target_fiedler = 0.5):
    graph = np.array([np.array([0 if i == j else 1 for j in range(size)]) for i in range(size)])
    subgraph = SpecifyRandom(graph, fiedler).create_graph(target_fiedler, bound="one", runs=1)
    return subgraph


def simulate(forms, parameter_trials):
    # 
    # Run Simulations
    # 

    dash = '-' * 40
    columns = ["Formation", "Algorithm", "Target λ", "Side", "Result λ", "Result ν", "Edges"]
    print(dash)
    print('{:<24s}{:<32s}{:<8s}{:<8s}{:<10s}{:<10s}{:<20s}'.format(*columns))
    print(dash)

    # Preload classes to allow decision tree to make only once

    meta_stats = {}
    for formation in forms:
        alg_results = OrderedDict()

        test_types = [
            # TestSpecifyDecisionTree(formation, fiedler, bound="one", target_connectivity=min(parameter_trials)),
            TestSpecifyRandom(formation, fiedler, "one"),
            TestSpecifySmallStep(formation, fiedler, "one"),
            TestSpecifyBigStep(formation, fiedler, "one"),
            TestSpecifySmallLeverage(formation, fiedler, "one"),
            TestSpecifyLargeLeverage(formation, fiedler, "one"),
            TestSpecifySmallGradient(formation, fiedler, "one"),
            TestSpecifyLargeGradient(formation, fiedler, "one"),
        ]

        test = TestFull(formation)
        (test,graph) = (test, test.create_graph(None))
        nf = fiedler(graph.adj_matrix)
        print('{:<24s}{:<32s}{:<8s}{:<8s}{:<10.4f}{:<10.4f}{:<20s}'.format(formation["name"], test.name, str(test.target_connectivity), test.bound, fiedler(graph.adj_matrix), normalized_fiedler(graph.adj_matrix), str(get_edges(graph.adj_matrix))))
        print()

        trials = parameter_trials

        for x in trials:
            for t_f in test_types:
                test = t_f
                (test,graph) = (test, test.create_graph(x))

                # Better print formatting 
                # https://scientificallysound.org/2016/10/17/python-print3/
                tnf = fiedler(graph.adj_matrix)
                
                test_n = (test.name,getattr(test, "color", None))
                if test_n not in alg_results: alg_results[test_n] = {}
                if x not in alg_results[test_n]: alg_results[test_n][x] = {}
                alg_results[test_n][x] = tnf
                
                print('{:<24s}{:<32s}{:<8s}{:<8s}{:<10.4f}{:<10.4f}{:<20s}'.format(formation["name"], test.name, str(x), test.bound, fiedler(graph.adj_matrix), tnf, str(get_edges(graph.adj_matrix))))
                if test_n not in meta_stats:
                    meta_stats[test_n] = {"edges" : 0}
                meta_stats[test_n]["edges"] += (len(get_edges(formation["full"])) - len(get_edges(graph.adj_matrix)))
            print()
            
        plot_bar_alg(alg_results,parameter_trials, formation, "compare_algorithms_round-1")

    print()
    print("META STATS")
    print("\t Edges:")
    for (name,color), value in meta_stats.items():
        print('\t\t{:<32s}{:<5d}'.format(name, value["edges"]))

if __name__ == "__main__":

    import timeit
    start = timeit.default_timer()


    
    # 
    # Arguments
    # 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--formation", type=int, help="enter a formation number/id",
                        nargs='?', default=0, const=0, choices=range(-1, len(formations) + 1))
    args = parser.parse_args()

    # To Create a Formation, add one to `formations.py`
    if args.formation == -1:
        forms = []
    elif args.formation == 0:
        forms = formations
    else: 
        form = formations[args.formation - 1]
        forms = [form]

    

    # To Create a New Test
    # ... create a class with a `create_graph` method and a name property
    # ... that takes in a formation and outputs a Graph object
    # Then add Test Class to Array
    # ... each test will be supplied a formation based on the args

    
    # parameter_trials = [0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.75, 1]
    # parameter_trials += [1.25, 1.5,1.75,2,2.5]


    parameter_trials = [0.45, 0.6, 1, 1.25, 1.75, 2, 2.5]

    simulate(forms, parameter_trials)
    
    # additional = []
    # for size in range(10,20,10):
    #     simulate([{
    #         "name": "n = {} and λ ≈ {}".format(size,round(10,2)),
    #         "nodes": [None, None],
    #         "full": random_graph(size, 10)
    #     }], parameter_trials)

    stop = timeit.default_timer()
    print('Time: ', stop - start)  

    