## Brief explanation of algorithm
Algorithm determines whether a graph contains a subgraph
that is equivalent to a smaller input graph based on edge values
and the general shape of the subgraph.

It accomplishes this via three stages:

### STAGE 1
For each node in the input graph, randomly select
a node from the main graph that contains the same or
more edges as the input graph node

### STAGE 2
Check if the adjacency matrix of the selected subgraph
**contains** the adjacency matrix of the input graph (whether
the subgraph's matrix contains ones in the same positions as the
input graph's matrix but still contains ones in other positions)

### STAGE 3
Check if the set of edge values in each of the nodes in the **input graph**
is a subset of any of the set of edge values in each of the **subgraph nodes**
