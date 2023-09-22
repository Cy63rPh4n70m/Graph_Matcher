#########################################
# main subgraph matching code
# is in match_sub_graph(self)
#########################################
import os
import random
import math
import numpy as np
from tqdm import tqdm
from copy import deepcopy

class Graph:
    def __init__(self, input_file):
        # dictionary containing all nodes of graph
        self.all_nodes = {}
        self.node_indexes = {}

        self.__load_file(input_file)
    
    def __load_file(self, path):
        with open(path, "r") as f:
            lines = f.readlines()
        
        # obtain node names and connections as list
        node_names = [line.split("|")[0] for line in lines]
        connections = [(line.split("|")[1])
                       .replace("\n","")
                       .split(" ")
                       for line in lines]
        
        for i, (node_name, connection) in enumerate(zip(node_names, connections)):
            self.all_nodes.update({node_name: connection})
            self.node_indexes.update({node_name: i})
        
        self.node_indexes = self.generate_node_index_dict(self.all_nodes)
    
    def generate_node_index_dict(self, node_dict):
        node_indexes = {}
        for i, (node_name, connection) in enumerate(node_dict.items()):
            node_indexes.update({node_name: i})
        return node_indexes
    
    def display(self):
        for entry in self.all_nodes.items():
            print(entry)
    
    def display_adj_matrix(self):
        matrix = self.get_adjacency_matrix(self.all_nodes, self.node_indexes)
        print("  ", end="")
        for name in self.node_indexes.keys():
            print(name, end=" ")
        print("")

        for node_name, i in self.node_indexes.items():
            print(node_name + " ", end="")

            for j in range(len(self.node_indexes)):
                if matrix[i][j] == 1:
                    print(f"\033[47;30m{matrix[i][j]}\033[0m", end=" ")
                else:
                    print(f"{matrix[i][j]}", end=" ")

            print("")
    
    def get_adjacency_matrix(self, node_dict, node_indexes):
        # create the matrix
        matrix = np.zeros(shape=(len(node_dict), len(node_dict)), dtype=int)

        # loop through the names and connections 
        for node_name, connections in node_dict.items():

            # obtain the index of the node via second dictionary for
            # node name
            index1 = node_indexes.get(node_name)

            # loop through the node names in the connection list
            for connection in connections:
                # obtain only the node name
                connection_node_name = connection.split(":")[0]
                index2 = node_indexes.get(connection_node_name)

                matrix[index1][index2] = 1

        return matrix
    
    def prune_graph(self, node_dict: dict, node_indexes):
        new_node_dict = deepcopy(node_dict)
        for node_name, connections in new_node_dict.items():
            
            new_connections = []
            # loop through the node names in the connection list
            for connection in connections:
                # obtain only the node name
                connection_node_name = connection.split(":")[0]
                index2 = node_indexes.get(connection_node_name)
                
                # prunes connections that go to other nodes
                # that aren't included in the graph
                if index2 is not None:
                    new_connections.append(connection)
                    
            new_node_dict[node_name] = new_connections.copy()
        
        return new_node_dict
    
    def match_sub_graph(self, input_graph):
        input_graph_nodes = input_graph.all_nodes
        
        matching_graphs = []

        # if number of nodes in main graph is lesser than the number 
        # of subgraph, return False
        if len(self.all_nodes) < len(input_graph_nodes):
            return matching_graphs

        # generate adjacency matrix for the smaller graph
        sub_node_indexes = self.generate_node_index_dict(input_graph_nodes)
        subgraph_adj = self.get_adjacency_matrix(input_graph_nodes, sub_node_indexes)

        # create connection edge value 2d list
        # used for stage three
        small_graph_edge_v_2d = []
        for connections in input_graph_nodes.values():
            edge_val_list = [connection.split(":")[1]
                             for connection in connections]
            small_graph_edge_v_2d.append(edge_val_list)

        # prevents indefinite loop if subgraph
        # cannot be found (using formula for permutation)
        total = len(self.all_nodes) + len(input_graph_nodes)
        subgraph_len = len(input_graph_nodes)
        max_loop = math.factorial(total) / math.factorial(total - subgraph_len)

        for i in tqdm(range(int(max_loop))):
            selected_main_nodes = []

            # STAGE 1
            # for each of the nodes in the sub graph
            # find another corresponding node in main graph that
            # has equal or more number of edges as the subgraph node
            # main_graph_node[0] refers to the node name
            # main_graph_node[1] refers to list of connected nodes
            for input_graph_node in input_graph_nodes.items():
                while True:
                    main_graph_node = random.choice(list(self.all_nodes.items()))
                    # check that main graph node has equal or more connections
                    # to the input graph node and the node has not already 
                    # been selected
                    if (len(main_graph_node[1]) >= len(input_graph_node[1]) and
                        main_graph_node not in selected_main_nodes):
                        # select the main graph node
                        selected_main_nodes.append(main_graph_node)
                        # move to next input graph node
                        break
                    else:
                        # choose a new random node from main graph
                        pass
                        
            # create adjacency matrix for the selected subgraph from
            # main graph, connections that point to nodes that aren't
            # part the subgraph are ignored
            selected_main_nodes = dict(selected_main_nodes)
            selected_node_indexes = self.generate_node_index_dict(selected_main_nodes)

            # remove connections to nodes that are not included in the 
            # selected subgraph
            selected_main_nodes = self.prune_graph(
                selected_main_nodes, selected_node_indexes
                )
            
            selected_adj = self.get_adjacency_matrix(selected_main_nodes, selected_node_indexes)

            # STAGE 2
            # compare adjacency matrices of the smaller graph and the
            # subgraph

            # subtract the matrix of the selected graph by the matrix 
            # of the subgraph to check if all values are non zero, 
            # (this allows for "sub adjacency" matrices)
            diff_matrix = selected_adj - subgraph_adj

            # check if result adjacency matrix contain negative values
            if not np.any(diff_matrix < 0):

                # STAGE 3
                # check if each node's edge values from the input graph are a
                # subset of any of the node's edge values in the valid subgraph
                all_edge_values_satisfied = []

                for selected_connection in selected_main_nodes.values():
                    # getting the edge values of the subgraph node
                    # as a list of values
                    edge_values = [connection.split(":")[1]
                                   for connection in selected_connection]

                    # for each edge value list from each node of the input
                    # graph
                    has_edge_values = False
                    for small_edge_v_list in small_graph_edge_v_2d:
                        # check that list of edge values in any node of input graph is
                        # a subset of the list of edge values in the selected subgraph
                        if all(e_v in edge_values for e_v in small_edge_v_list):
                            has_edge_values = True
                            break

                    # add the boolean variable
                    all_edge_values_satisfied.append(has_edge_values)

                # prevent adding the same valid subgraph
                # as well as checking if the edge values of each node in the
                # input graph has been satisfied by the selected subgraph
                if all(all_edge_values_satisfied) and selected_main_nodes not in matching_graphs:
                    matching_graphs.append(selected_main_nodes)
            
            else:
                # skip the selected subgraph
                pass

        return matching_graphs

if __name__ == "__main__":
    # for testing subgraph matching algorithm
    # paths to adjacency lists of graph files
    # change directories to test different graphs and subgraphs
    graph = Graph("test_cases/large_graphs/graph.txt")
    subgraph = Graph("test_cases/large_graphs/input_graph.txt")

    print("Adjacency matrix of entire main graph:")
    print("(Algorithm doesn't utilize this specific matrix for comparison)")
    graph.display_adj_matrix()
    print("Adjacency matrix of subgraph:")
    subgraph.display_adj_matrix()
    matching_graphs = graph.match_sub_graph(subgraph)
    for i, matching_graph in enumerate(matching_graphs, 1):
        print(f"Matching sub graph {i}:")
        for node in matching_graph.items():
            print(node)
        print("")
    
    if matching_graphs:
        result = True
    else:
        result = False

    print(f"Graph contains subgraph/s: {result}")
