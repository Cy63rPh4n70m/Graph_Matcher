## Requirements
Requires Python 3.11.0  
To install module requirements execute `pip install -r requirements.txt`

## Running the code
To test the algorithm on graphs from `test_cases/` run `python main.py`
Test cases contain images of the graphs for validation of results.
(The path to different test cases can be altered at the bottom of
 the `main.py` in `if __name__ == '__main__'` where the `Graph` objects are created.)

(Graphs are stored in text files in the form of adjacency lists with a colon
 separating the connection names and edge values for each node. Each connection
 is separated by a space.)

## Brief explanation of algorithm
(The main algorithm for graph matching is in the function `match_sub_graph()`)

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
the input graph node. Nodes are selected without replacement. The selected
nodes become a subgraph.

### STAGE 2
Check if the adjacency matrix of the selected subgraph
**contains** the adjacency matrix of the input graph (the subgraph's matrix contains 1s
in the same positions as the input graph's matrix but may also contain extra 1s in other positions).
The algorithm does this by subtracting the matrix of the subgraph by
the matrix of the input graph and validates the connectedness of the subgraph when
the resulting matrix is non-negative (all **essential** node connections are satisfied.)

### STAGE 3
For each node in the **input graph**, the algorithm obtains the edge values of the input node as a list and
loops through every node of the subgraph, checking if all values in the list is **contained** in at least
one of the **subgraph nodes**. This stage filters out subgraphs that have the same node connectedness
but different edge values.

If the subgraph satisfies all three stages, it is added to the `matching_graphs` list.  
The above stages are repeated for a finite number of times to try different combinations of selected nodes.
The algorithm at the end returns the list containing any subgraphs that match the input graph, and accepts
if the list **is not** empty and rejects otherwise.
