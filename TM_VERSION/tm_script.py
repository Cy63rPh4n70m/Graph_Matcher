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
input_graph_index = 1
# tape for main graph
main_graph_tape = np.full(shape=(1000), fill_value='_', dtype=str)
main_graph_index = 1
# tape containing all labels of input graph
input_labels_tape = np.full(shape=(100), fill_value='_', dtype=str)
input_labels_index = 1
# tape containing all labels of main graph
main_labels_tape = np.full(shape=(100), fill_value='_', dtype=str)
main_labels_index = 1
# tape containing all labels of sub graph
sub_labels_tape = np.full(shape=(100), fill_value='_', dtype=str)
sub_labels_index = 1

# tape to store temporary label, only used for permutation 1
permutation_tape_temp = np.full(shape=(100), fill_value='_', dtype=str)
permutation_tape_temp_index = 1

# stores all possible input graph connections
input_permutation_tape1 = np.full(shape=(100), fill_value='_', dtype=str)
input_permutation_tape1_index = 1
input_permutation_tape2 = np.full(shape=(100), fill_value='_', dtype=str)
input_permutation_tape2_index = 1

# stores all possible aub graph connections
sub_permutation_tape1 = np.full(shape=(100), fill_value='_', dtype=str)
sub_permutation_tape1_index = 1
sub_permutation_tape2 = np.full(shape=(100), fill_value='_', dtype=str)
sub_permutation_tape2_index = 1

# tape for adj matrix of input graph
input_matrix_tape = np.full(shape=(1000), fill_value='_', dtype=str)
input_matrix_index = 1
# tape for adj matrix of sub graph
sub_matrix_tape = np.full(shape=(1000), fill_value='_', dtype=str)
sub_matrix_index = 1

# tape for matching sub graphs
matching_graphs_tape = np.full(shape=(1000), fill_value='_', dtype=str)
matching_graphs_index = 1

boolean_tape = np.full(shape=(5), fill_value='_', dtype=str)
boolean_tape_index = 1

# load main graph and input graph
with open("tm_graphs/input_graph_large.txt", "r") as f:
    input_graph_text = f.read().replace("\n","")
with open("tm_graphs/main_graph_large.txt", "r") as f:
    main_graph_text = f.read().replace("\n","")
# write the graphs to the tapes
for char in input_graph_text:
    input_graph_tape[input_graph_index] = char
    input_graph_index += 1
for char in main_graph_text:
    main_graph_tape[main_graph_index] = char
    main_graph_index += 1
input_graph_index = 1
main_graph_index = 1

#FOR INPUT TAPE#####################################################
# initialize graph labels for input graph
input_graph_index = 1
input_labels_index = 1
initialize_graph_label_tape(
    input_graph_tape, input_graph_index, input_labels_tape, input_labels_index
)
#print(input_labels_tape)

# creating adjacency matrix of input graph
################################################################################

# initalizing permutation1 and permutation2 tape for input graph
input_labels_index = 1
input_permutation_tape1_index = 1
input_permutation_tape2_index = 1
initialize_permutation_tapes(
    permutation_tape_temp, permutation_tape_temp_index,
    input_labels_tape, input_labels_index, 
    input_permutation_tape1, input_permutation_tape1_index,
    input_permutation_tape2, input_permutation_tape2_index
)

# generate adjacency matrix of input graph
#print(input_graph_tape)

# create adjacency matrix of input graph
input_graph_index = 1
input_matrix_index = 1
input_permutation_tape1_index = 1
input_permutation_tape2_index = 1
boolean_tape_index = 1
create_adjacency_matrix(
    input_graph_tape, input_graph_index,
    input_matrix_tape, input_matrix_index,
    input_permutation_tape1, input_permutation_tape1_index,
    input_permutation_tape2, input_permutation_tape2_index,
    boolean_tape, boolean_tape_index
)

#FOR SUBGRAPH#####################################
# get subgraph of main graph
# initialize graph labels for main graph
main_graph_index = 1
main_labels_index = 1
initialize_graph_label_tape(
    main_graph_tape, main_graph_index, main_labels_tape, main_labels_index
)

for i in tqdm(range(1000)):
    main_labels_index = 1
    input_labels_index = 1
    sub_labels_index = 1
    initialize_sub_labels_tape(
        main_labels_tape, main_labels_index, input_labels_tape, input_labels_index,
        sub_labels_tape, sub_labels_index
    )
    #print(sub_labels_tape)

    # initalizing permutation1 and permutation2 tape for sub graph
    sub_labels_index = 1
    sub_permutation_tape1_index = 1 
    sub_permutation_tape2_index = 1
    initialize_permutation_tapes(
        permutation_tape_temp, permutation_tape_temp_index,
        sub_labels_tape, sub_labels_index, 
        sub_permutation_tape1, sub_permutation_tape1_index,
        sub_permutation_tape2, sub_permutation_tape2_index
    )
    #print(sub_permutation_tape1)
    #print(sub_permutation_tape2)

    # create adjacency matrix of input graph
    main_graph_index = 1
    sub_matrix_index = 1
    sub_permutation_tape1_index = 1
    sub_permutation_tape2_index = 1
    boolean_tape_index = 1
    create_adjacency_matrix(
        main_graph_tape, main_graph_index,
        sub_matrix_tape, sub_matrix_index,
        sub_permutation_tape1, sub_permutation_tape1_index,
        sub_permutation_tape2, sub_permutation_tape2_index,
        boolean_tape, boolean_tape_index
    )
    #print(sub_matrix_tape)

    # check if the adjacency matrices are equal, if yes, write
    # '1' to boolean tape, otherwise '0'
    input_matrix_index = 1
    sub_matrix_index = 1
    compare_adjacency_matrices(
        input_matrix_tape, input_matrix_index,
        sub_matrix_tape, sub_matrix_index,
        boolean_tape, boolean_tape_index
    )

    adj_matrices_match = boolean_tape[boolean_tape_index] == '1'
    if adj_matrices_match:
        sub_matrix_index = 1
        sub_permutation_tape1_index = 1
        sub_permutation_tape2_index = 1
        matching_graphs_index = copy_subgraph_to_result(
            sub_matrix_tape, sub_matrix_index,
            sub_permutation_tape1, sub_permutation_tape1_index,
            sub_permutation_tape2, sub_permutation_tape2_index,
            matching_graphs_tape, matching_graphs_index
        )

    # clear the sub matrix tape
    reset_tape(sub_matrix_tape, sub_matrix_index)
    # clear the sub labels tape
    reset_tape(sub_labels_tape, sub_labels_index)
    # clear the sub permutation tapes
    reset_tape(sub_permutation_tape1, sub_permutation_tape1_index)
    reset_tape(sub_permutation_tape2, sub_permutation_tape2_index)

print("Main graph: ")
print("".join(list(main_graph_tape)))
print("Input graph: ")
print("".join(list(input_graph_tape)))
print("Matching graphs:")
print("".join(list(matching_graphs_tape)))