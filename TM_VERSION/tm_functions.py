import random

def initialize_graph_label_tape(graph_tape, graph_index, labels_tape, labels_index):
    labels_index -= 1
    
    while True:
        if graph_tape[graph_index] == '_':
            break
        # if tape reads pipe, move back one and write char
        # from graph tape to labels tape
        if graph_tape[graph_index] == '|':
            
            # move input graph tape left
            graph_index -= 1

            # do not write to input label tape if the same node label read
            # from input graph
            if labels_tape[labels_index] == graph_tape[graph_index]:
                pass
            else:
                # move input label tape right
                labels_index += 1
                labels_tape[labels_index] = graph_tape[graph_index]
            
            # move input graph tape right so its on pipe char
            graph_index += 1
        
        # move input graph tape right
        graph_index += 1

    #################################################
    # index is passed by value, original index
    # still at 1
    # move input labels tape to right until blank
    while labels_tape[labels_index] != '_':
        labels_index -= 1
    labels_index += 1

    # move input graph tape to right until blank
    graph_index -= 1
    while graph_tape[graph_index] != '_':
        graph_index -= 1
    graph_index += 1

def initialize_permutation_tapes(
        permutation_tape_temp, permutation_tape_temp_index,
        labels_tape, labels_index, 
        permutation_tape1, permutation_tape1_index,
        permutation_tape2, permutation_tape2_index
):
    # initialize permutation1 tape
    # label tape is used to keep count
    permutation_tape_temp[permutation_tape_temp_index] = labels_tape[labels_index]
    while True:

        # move label tape left to beginning
        while labels_tape[labels_index] != '_':
            labels_index -= 1
        labels_index += 1

        while True:
            # to keep count
            if labels_tape[labels_index] == '_':
                labels_index -= 1
                break
            
            else:
                permutation_tape1[permutation_tape1_index] = permutation_tape_temp[permutation_tape_temp_index]
                permutation_tape1_index += 1
                labels_index += 1
        
        # move left until input labels has encountered the same label as the temp permutation
        while labels_tape[labels_index] != permutation_tape_temp[permutation_tape_temp_index]:
            labels_index -= 1
        labels_index += 1 # moves the label tape to the next character

        if labels_tape[labels_index] == '_':
            break
        
        # set permutation tape to next label in label tape
        permutation_tape_temp[permutation_tape_temp_index] = labels_tape[labels_index]

    #initialize permutation2 tape for graph
    # move input label tape left
    labels_index -= 1
    while labels_tape[labels_index] != '_':
        labels_index -= 1
    labels_index += 1

    # move input permutation 1 to right
    permutation_tape1_index -= 1
    while permutation_tape1[permutation_tape1_index] != '_':
        permutation_tape1_index -= 1
    permutation_tape1_index += 1

    while True:
        permutation_tape2[permutation_tape2_index] = labels_tape[labels_index]
        permutation_tape2_index += 1
        permutation_tape1_index += 1 # for counting length of permutation 2 tape
        labels_index += 1

        if labels_tape[labels_index] == '_':
            # move input label tape left
            labels_index -= 1
            while labels_tape[labels_index] != '_':
                labels_index -= 1
            labels_index += 1
        
        if permutation_tape1[permutation_tape1_index] == '_':
            break

    ###################################################
    # index is still at 1 (passed by value)
    # move input permutation 1 left
    permutation_tape1_index -= 1
    while permutation_tape1[permutation_tape1_index] != '_':
        permutation_tape1_index -= 1
    permutation_tape1_index += 1

    # move input permutation 2 left
    permutation_tape2_index -= 1
    while permutation_tape2[permutation_tape2_index] != '_':
        permutation_tape2_index -= 1
    permutation_tape2_index += 1

def initialize_graphs_tape(
    graph_tape, graph_index,
    temp_conn_tape, temp_conn_tape_index
):

    # for each graph in graph
    while True:
        if graph_tape[graph_index] == '_':
            break

        if graph_tape[graph_index] == '|':

            # move tape head to left of | 
            graph_index -= 1
            temp_conn_tape[temp_conn_tape_index] = graph_tape[graph_index]
            graph_index += 2 # move tape head to right of | 
            temp_conn_tape_index += 1

            temp_conn_tape[temp_conn_tape_index] = graph_tape[graph_index]
            temp_conn_tape_index += 1
            temp_conn_tape[temp_conn_tape_index] = '|'
            temp_conn_tape_index += 1
        
        graph_index += 1
    
    return graph_index, temp_conn_tape_index

def create_adjacency_matrix(
    graph_tape, graph_tape_index,
    adjacency_matrix_tape, adjacency_matrix_tape_index,
    permutation1_tape, permutation1_tape_index,
    permutation2_tape, permutation2_tape_index,
    boolean_tape, boolean_tape_index
):
    # initalize adjacency list to zeros, using permutation tape 1
    # to get sense of length
    while permutation1_tape[permutation1_tape_index] != '_':
        adjacency_matrix_tape[adjacency_matrix_tape_index] = '0'
        permutation1_tape_index += 1
        adjacency_matrix_tape_index += 1
    
    permutation1_tape_index = 1
    adjacency_matrix_tape_index = 1


    while True: 
        # if reached end of graph tape
        if graph_tape[graph_tape_index] == '_':
            break

        if graph_tape[graph_tape_index] == '|':
            permutation1_tape_index = 1
            permutation2_tape_index = 1
            adjacency_matrix_tape_index = 1

            while True:
                # write zeros to boolean tape
                boolean_tape[boolean_tape_index] = '0'
                boolean_tape_index += 1
                boolean_tape[boolean_tape_index] = '0'
                boolean_tape_index -= 1

                # move graph tape back one
                graph_tape_index -= 1
                
                # if label of left is equal to the label in permutation 1, write 1
                # to boolean tape
                if graph_tape[graph_tape_index] == permutation1_tape[permutation1_tape_index]:
                    boolean_tape[boolean_tape_index] = '1'
                else:
                    boolean_tape[boolean_tape_index] = '0'

                boolean_tape_index += 1 # move boolean tape right
                graph_tape_index += 2 # move to right label

                # if label of right is equal to the label in permutation 2, write 1
                # to boolean tape
                if graph_tape[graph_tape_index] == permutation2_tape[permutation1_tape_index]:
                    boolean_tape[boolean_tape_index] = '1'
                else:
                    boolean_tape[boolean_tape_index] = '0'
                boolean_tape_index = 1 # move boolean tape to start

                # check if boolean tape only has 1s
                # if yes, write 1 to the adjacency matrix tape,
                # otherwise ignore
                if boolean_tape[boolean_tape_index] == '1':
                    boolean_tape_index += 1
                    if boolean_tape[boolean_tape_index] == '1':
                        adjacency_matrix_tape[adjacency_matrix_tape_index] = '1'
                    else:
                        pass
                else:
                    pass
                
                # reset boolean tape to beginning
                boolean_tape_index = 1
                
                # move to next permutation
                permutation1_tape_index += 1
                permutation2_tape_index += 1
                adjacency_matrix_tape_index += 1
                
                # if reach end of all permutations
                if permutation1_tape[permutation1_tape_index] == '_':
                    break

                graph_tape_index -= 1
            
            # move graph tape onto the | char, which will be
            # move right again
            graph_tape_index += 1

        # move graph tape right
        graph_tape_index += 1

def initialize_sub_labels_tape(
    main_labels_tape, main_labels_idx, # whole graph to select random labels from
    input_labels_tape, input_labels_idx, # for determining the length of sub graph
    sub_labels_tape, sub_labels_idx,
):
    
    # in case the sub graph tape is not clear
    # clear everything and move to beginning
    if sub_labels_tape[sub_labels_idx] == '_':
        sub_labels_idx -= 1
    while sub_labels_tape[sub_labels_idx] != '_':
        sub_labels_tape[sub_labels_idx] = '_'
        sub_labels_idx -= 1
    sub_labels_idx += 1

    # loop through main labels
    # allowed to reselect the same labels for simplicity
    main_labels_idx += 1
    while True:

        if random.randint(0, 1) == 1: # randomly select the label
            sub_labels_tape[sub_labels_idx] = main_labels_tape[main_labels_idx]

            sub_labels_idx += 1
            input_labels_idx += 1
            # check if sub labels has reached the length of the input labels
            if (sub_labels_tape[sub_labels_idx] == '_' and
                input_labels_tape[input_labels_idx] == '_'):
                break # stop looping and exit function

            else:
                pass

        else:
            pass

        main_labels_idx += 1

        # move main labels tape back to beginning
        # if not enough sub labels have been selected
        if main_labels_tape[main_labels_idx] == '_':
            main_labels_idx -= 1
            while main_labels_tape[main_labels_idx] != '_':
                main_labels_idx -= 1
            main_labels_idx += 1

def compare_adjacency_matrices(
    adj_matx1, adj_matx1_idx,
    adj_matx2, adj_matx2_idx,
    boolean_tape, boolean_tape_idx
):

    # initialize boolean tape to true
    boolean_tape[boolean_tape_idx] = '1'

    while True:
        if adj_matx1[adj_matx1_idx] == '_' and adj_matx2[adj_matx2_idx] == '_':
            break
        elif adj_matx1[adj_matx1_idx] == adj_matx2[adj_matx2_idx]:
            pass
        else:
            boolean_tape[boolean_tape_idx] = '0'
            break
        adj_matx1_idx += 1
        adj_matx2_idx += 1
    
def reset_tape(
    tape, idx
):
    # move to end of tape
    while tape[idx] != '_':
        idx += 1
    idx -= 1

    # reset to _ until beginning
    while tape[idx] != '_':
        tape[idx] = '_'
        idx -= 1

def copy_subgraph_to_result(
    sub_matrix, sub_matrix_index,
    permutation1, permutation1_idx,
    permutation2, permutation2_idx,
    matching_graph_tape, matching_graph_tape_idx
):
    
    while True:
        if sub_matrix[sub_matrix_index] == '_':
            break

        elif sub_matrix[sub_matrix_index] == '1':
            matching_graph_tape[matching_graph_tape_idx] = permutation1[permutation1_idx]
            matching_graph_tape_idx += 1
            matching_graph_tape[matching_graph_tape_idx] = permutation2[permutation2_idx]
            matching_graph_tape_idx += 1
            matching_graph_tape[matching_graph_tape_idx] = ','
            matching_graph_tape_idx += 1
        
        elif sub_matrix[sub_matrix_index] == '0':
            pass

        sub_matrix_index += 1
        permutation1_idx += 1
        permutation2_idx += 1
    
    matching_graph_tape[matching_graph_tape_idx] = '#'
    matching_graph_tape_idx += 1

    return matching_graph_tape_idx
