## Requirements
To install requirements execute `pip install -r requirements.txt`

## Running the code
To test the algorithm on graphs from `test_cases/` run `python main.py`

## Brief explanation of algorithm
This algorithm determines whether a graph contains a subgraph
that is equivalent to a smaller input graph based on edge values
and the connectiveness.

(The stages are explained in more detail in the comments of `main.py`)

It accomplishes this via three stages:

### STAGE 1
For each node in the input graph, randomly select
a node from the main graph that contains the same or
more edges as the input graph node.

### STAGE 2
Check if the adjacency matrix of the selected subgraph
**contains** the adjacency matrix of the input graph (whether
the subgraph's matrix contains ones in the same positions as the
input graph's matrix but still contains ones in other positions).
The algorithm performs this by subtracting the matrix of the subgraph by
the matrix of the input graph and validates the shape of the subgraph when
there are no negative ones.

### STAGE 3
The algorithm checks if the set of edge values in each of the nodes in the **input graph**
is a subset of any of the set of edge values in each of the **subgraph nodes**.
