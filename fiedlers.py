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

import matplotlib._color_data as mcd


def plot_alg(data):
    
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(plt.NullFormatter())
    i = 0
    for n,(form,options) in data.items():
        x = list(i for _ in form)
        y = list(form)
        name = n + " ({} Unique Fiedlers - {} Configurations)".format(len(y), options)
        ax.scatter(x, y, c=list(mcd.XKCD_COLORS.values())[i].upper(), label=name,
                alpha=0.5, edgecolors='none')
        i += 1

    ax.legend()
    ax.grid(True)

    plt.show()



if __name__ == "__main__":
    
    # 
    # Arguments
    # 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--formation", type=int, help="enter a formation number/id",
                        nargs='?', default=0, const=0, choices=range(0, len(formations) + 1))
    args = parser.parse_args()

    # To Create a Formation, add one to `formations.py`
    if args.formation == 0:
        forms = formations
    else: 
        form = formations[args.formation - 1]
        forms = [form]
 

    # 
    # Run Simulations
    # 

    import timeit
    start = timeit.default_timer()

    # Preload classes to allow decision tree to make only once

    results = {}
    alg_results = OrderedDict()
    for formation in forms:
        alg = SpecifyDecisionTree(formation["full"], fiedler, 0, "one")
        results[formation["name"]] = (alg.possibilities(),len(alg.options))
        

    plot_alg(results)
    stop = timeit.default_timer()
    print('Time: ', stop - start)  