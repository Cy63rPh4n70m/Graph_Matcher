## Requirements
Requires Python 3.11.0  
To install module requirements execute `pip install -r requirements.txt`

## Running the code
To test the algorithm on graphs from `test_cases/` run `python main.py`
Test cases contain images of the graphs for validation of results.
(The path to different test cases can be altered at the bottom of
 the `main.py` where the `Graph` objects are created.)

(Graphs are stored in text files in the form of adjacency lists with a colon
 separating the connection names and edge values for each node. Each connection
 is separated by a space.)

## Brief explanation of algorithm
This algorithm determines whether an input graph is included in a larger graph
based on edge values and the node connectedness, and returns all
subgraphs that match the input graph.

**(The stages are explained in more detail in the comments of `main.py`)**

It accomplishes this via three stages:

### STAGE 1
(If the main graph has less nodes than the input graph, the algorithm
 returns False.)

For each node in the input graph, the algorithm randomly selects
a node from the main graph that contains the same or more edges as
the input graph node. Nodes are selected without replacement.

### STAGE 2
Check if the adjacency matrix of the selected subgraph
**contains** the adjacency matrix of the input graph (whether
the subgraph's matrix contains ones in the same positions as the 
input graph's matrix but still contains ones in other positions).
The algorithm performs this by subtracting the matrix of the subgraph by
the matrix of the input graph and validates the connectedness of the subgraph when
the resulting matrix is non-negative (all **necessary** node connections are satisfied.)

### STAGE 3
For each node in the **input graph**, the algorithm obtains the edge values of the input node as a list and
loops through every node of the subgraph, checking if all values in the list is **contained** in
the **subgraph nodes** edge values. This stage filters out subgraphs that have the same node connectedness
but different edge values.
