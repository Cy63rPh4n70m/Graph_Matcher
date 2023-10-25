import numpy as np
import random
from tm_functions import *
from tqdm import tqdm

'''
EDGE VALUES ARE ASSUMED TO BE INTEGERS

graph format
A|B:1,A|C:2
assume labels and edge values are of only one character

adj matrix format
  ABC
A 001
B 101
C 110

converts to 001101110
permutation1: AAABBBCCC
permutation2: ABCABCABC
'''

# initialize tapes

# tape for input graph
input_graph_tape = np.full(shape=(1000), fill_value='_', dtype=str)
input_graph_pos = 1
# tape for main graph
main_graph_tape = np.full(shape=(1000), fill_value='_', dtype=str)
main_graph_pos = 1
# tape containing all labels of input graph
input_labels_tape = np.full(shape=(100), fill_value='_', dtype=str)
input_labels_pos = 1
# tape containing all labels of main graph
main_labels_tape = np.full(shape=(100), fill_value='_', dtype=str)
main_labels_pos = 1
# tape containing all labels of sub graph
sub_labels_tape = np.full(shape=(100), fill_value='_', dtype=str)
sub_labels_pos = 1

# tape to store temporary label, only used for permutation 1
permutation_tape_temp = np.full(shape=(100), fill_value='_', dtype=str)
permutation_tape_temp_pos = 1

# stores all possible input graph connections
input_permutation_tape1 = np.full(shape=(100), fill_value='_', dtype=str)
input_permutation_tape1_pos = 1
input_permutation_tape2 = np.full(shape=(100), fill_value='_', dtype=str)
input_permutation_tape2_pos = 1

# stores all possible sub graph connections
sub_permutation_tape1 = np.full(shape=(100), fill_value='_', dtype=str)
sub_permutation_tape1_pos = 1
sub_permutation_tape2 = np.full(shape=(100), fill_value='_', dtype=str)
sub_permutation_tape2_pos = 1

# tape for adj matrix of input graph
input_matrix_tape = np.full(shape=(100), fill_value='_', dtype=str)
input_matrix_pos = 1
# tape for adj matrix of sub graph
sub_matrix_tape = np.full(shape=(100), fill_value='_', dtype=str)
sub_matrix_pos = 1

# contains connection values of label connections in input graph
input_conn_value_tape = np.full(shape=(100), fill_value='_', dtype=str)
input_conn_value_pos = 1

# connection values for sub graph
sub_conn_value_tape = np.full(shape=(100), fill_value='_', dtype=str)
sub_conn_value_pos = 1

# tape for matching sub graphs
matching_graphs_tape = np.full(shape=(1000), fill_value='_', dtype=str)
matching_graphs_pos = 1

boolean_tape = np.full(shape=(5), fill_value='_', dtype=str)
boolean_tape_pos = 1

# load main graph and input graph
with open("tm_graphs/input_graph_large.txt", "r") as f:
    input_graph_text = f.read().replace("\n","")
with open("tm_graphs/main_graph_large.txt", "r") as f:
    main_graph_text = f.read().replace("\n","")
# write the graphs to the tapes
for char in input_graph_text:
    input_graph_tape[input_graph_pos] = char
    input_graph_pos += 1
for char in main_graph_text:
    main_graph_tape[main_graph_pos] = char
    main_graph_pos += 1
input_graph_pos = 1
main_graph_pos = 1

#FOR INPUT TAPE#####################################################
# initialize graph labels for input graph
input_graph_pos = 1
input_labels_pos = 1
initialize_graph_label_tape(
    input_graph_tape, input_graph_pos, input_labels_tape, input_labels_pos
)
#print(input_labels_tape)

# creating adjacency matrix of input graph
################################################################################

# initalizing permutation1 and permutation2 tape for input graph
input_labels_pos = 1
input_permutation_tape1_pos = 1
input_permutation_tape2_pos = 1
initialize_permutation_tapes(
    permutation_tape_temp, permutation_tape_temp_pos,
    input_labels_tape, input_labels_pos, 
    input_permutation_tape1, input_permutation_tape1_pos,
    input_permutation_tape2, input_permutation_tape2_pos
)

# generate adjacency matrix of input graph
#print(input_graph_tape)

# create adjacency matrix of input graph
input_graph_pos = 1
input_matrix_pos = 1
input_permutation_tape1_pos = 1
input_permutation_tape2_pos = 1
boolean_tape_pos = 1
create_adjacency_matrix(
    input_graph_tape, input_graph_pos,
    input_matrix_tape, input_matrix_pos,
    input_permutation_tape1_pos,
    input_permutation_tape1, input_permutation_tape2,
    boolean_tape, boolean_tape_pos
)

#FOR main graph#####################################
# label tape of main graph
main_graph_pos = 1
main_labels_pos = 1
initialize_graph_label_tape(
    main_graph_tape, main_graph_pos, main_labels_tape, main_labels_pos
)

# initialize the connection values in input graph
input_conn_value_pos = 1
input_graph_pos = 1
input_permutation_tape1_pos = 1
boolean_tape_pos = 1
initalize_graph_connection_values(
    input_conn_value_tape, input_conn_value_pos,
    input_graph_tape, input_graph_pos,
    input_permutation_tape1_pos, 
    input_permutation_tape1, input_permutation_tape2, 
    boolean_tape, boolean_tape_pos
)
#print("".join(input_conn_value_tape))
#print("".join(input_matrix_tape))
#print("".join(input_permutation_tape1))
#print("".join(input_permutation_tape2))

for i in tqdm(range(100)):
    main_labels_pos = 1
    input_labels_pos = 1
    sub_labels_pos = 1
    initialize_sub_labels_tape(
        main_labels_tape, main_labels_pos, input_labels_tape, input_labels_pos,
        sub_labels_tape, sub_labels_pos
    )
    #print(sub_labels_tape)

    # initalizing permutation1 and permutation2 tape for sub graph
    sub_labels_pos = 1
    sub_permutation_tape1_pos = 1 
    sub_permutation_tape2_pos = 1
    initialize_permutation_tapes(
        permutation_tape_temp, permutation_tape_temp_pos,
        sub_labels_tape, sub_labels_pos, 
        sub_permutation_tape1, sub_permutation_tape1_pos,
        sub_permutation_tape2, sub_permutation_tape2_pos
    )
    #print(sub_permutation_tape1)
    #print(sub_permutation_tape2)

    # create adjacency matrix of input graph
    # initialize the connection values in main graph
    sub_conn_value_pos = 1
    main_graph_pos = 1
    sub_permutation_tape1_pos = 1
    boolean_tape_pos = 1
    initalize_graph_connection_values(
        sub_conn_value_tape, sub_conn_value_pos,
        main_graph_tape, main_graph_pos,
        sub_permutation_tape1_pos, 
        sub_permutation_tape1, sub_permutation_tape2, 
        boolean_tape, boolean_tape_pos
    )

    main_graph_pos = 1
    sub_matrix_pos = 1
    sub_permutation_tape1_pos = 1
    sub_permutation_tape2_pos = 1
    boolean_tape_pos = 1
    create_adjacency_matrix(
        main_graph_tape, main_graph_pos,
        sub_matrix_tape, sub_matrix_pos,
        sub_permutation_tape1_pos,
        sub_permutation_tape1, sub_permutation_tape2,
        boolean_tape, boolean_tape_pos
    )

    # check if the adjacency matrices are equal, if yes, write
    # '1' to boolean tape, otherwise '0'
    input_matrix_pos = 1
    sub_matrix_pos = 1
    input_conn_value_pos = 1
    sub_conn_value_pos = 1
    compare_adjacency_matrices(
        input_matrix_tape, input_matrix_pos,
        sub_matrix_tape, sub_matrix_pos,
        input_conn_value_tape, input_conn_value_pos,
        sub_conn_value_tape, sub_conn_value_pos,
        boolean_tape, boolean_tape_pos
    )

    adj_matrices_match = boolean_tape[boolean_tape_pos] == '1'
    if adj_matrices_match:
        sub_matrix_pos = 1
        sub_permutation_tape1_pos = 1
        sub_permutation_tape2_pos = 1
        matching_graphs_pos = copy_subgraph_to_result(
            sub_matrix_tape, sub_matrix_pos,
            sub_permutation_tape1, sub_permutation_tape1_pos,
            sub_permutation_tape2, sub_permutation_tape2_pos,
            matching_graphs_tape, matching_graphs_pos
        )

    # clear the sub matrix tape
    reset_tape(sub_matrix_tape, sub_matrix_pos)
    # clear the sub labels tape
    reset_tape(sub_labels_tape, sub_labels_pos)
    # clear the sub permutation tapes
    reset_tape(sub_permutation_tape1, sub_permutation_tape1_pos)
    reset_tape(sub_permutation_tape2, sub_permutation_tape2_pos)

    # clear the sub conn tapes
    reset_tape(sub_conn_value_tape, sub_conn_value_pos)
    

print("Main graph: ")
print("".join(list(main_graph_tape)))
print("Input graph: ")
print("".join(list(input_graph_tape)))
print("Matching graphs:")
print("".join(list(matching_graphs_tape)))