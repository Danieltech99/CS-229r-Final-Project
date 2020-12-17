# CS-229r-Final-Project


*Abstract: Algebraic connectivity, as defined as the second smallest eigenvalue of the Laplacian, is a measure of connectivity. We study the problem of removing edges from a graph so as to approach a target connectivity and introduce a number of motivating use cases. We provide a simple framework that takes in a heuristic, a graph, and a target connectivity, then uses this heuristic to reduce the connectivity to arrive near the target value. We also show that this problem is NP-complete.*

Paper: [Investigating Methods of Reducing Algebraic Connectivity](paper/CS_229r_Final_Project.pdf)

Presentation: [CS 229r Final Project Presentation](paper/CS_229r_Final_Project_Presentation.pdf)

# Usage

Formations:
- 0: All
- 1: Circular
- 2: Wedge
- 3: Line


## Fiedlers Space Exploration
*Order of Runtime (with defaults): 1 minutes - x minutes*

This program uses the Decision Tree algorithm to perform an exhaustive search on each specified formation; this allows us to determine all unique graph configurations (subgraphs) and all unique Fiedler values; this is then plotted as a scatter plot.

***Warning:** this file uses the exhaustive search algorithm and thus is exponential in terms of the number of edges.*

```
python3 fiedlers.py --formation [0-3]
```
The optional formation flag allows you to specify which formation to run. The default (0) runs all formations.

### Configuring:

**Formations:** to change the formations being tested, add a formation to `formations.py`, making sure to follow the existing format.





## Compare Algorithms
*Order of Runtime (with defaults): 1 minutes - x minutes*

This file generates bar charts comparing the achieved Fiedler value of each algorithm compared to the exhaustive search for each algorithm. Generated graphs are commented out until enabled.

The program generates a number of semi-sparse graphs by starting with a fully connected graph of different numbers of nodes, which were passed to the Randomized algorithm with different target algebraic connectivity parameters.

***Warning:** this file can use the exhaustive search algorithm and thus is exponential in terms of the number of edges and the minimum target Fiedler value. Also large graphs can take a long time to evaluate even without the exhaustive search algorithm. Try not to test about n=50 unless running for hours.*

```
python3 app.py --formation [0-3]
```
The optional formation flag allows you to specify which formation to run in addition to the generated graphs (the circle formation takes the longest to run). The default (0) runs all formations.

### Configuring:

**Formations:** to change the formations being tested, add a formation to `formations.py`, making sure to follow the existing format.

**Target Fiedler Values:** to customize which target Fiedler values are being tested, edit the variable `parameter_trials`.

**Algorithms:** to change the algorithms being tested, in `app.py` create a class that extends `Test` like the other algorithms and has the method `create_graph` (see other algorithm test classes for constraints and parameters). Then add the class to the `test_types` list.

**Generated Graphs:** to change the generated graphs, modify the loop in __main__ that calls `random_graph`.