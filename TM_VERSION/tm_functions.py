import random

def initialize_graph_label_tape(graph_tape, graph_pos, labels_tape, labels_pos):
    labels_pos -= 1
    
    while True:
        if graph_tape[graph_pos] == '_':
            break
        # if tape reads pipe, move back one and write char
        # from graph tape to labels tape
        if graph_tape[graph_pos] == '|':
            
            # move input graph tape left
            graph_pos -= 1

            # do not write to input label tape if the same node label read
            # from input graph
            if labels_tape[labels_pos] == graph_tape[graph_pos]:
                pass
            else:
                # move input label tape right
                labels_pos += 1
                labels_tape[labels_pos] = graph_tape[graph_pos]
            
            # move input graph tape right so its on pipe char
            graph_pos += 1
        
        # move input graph tape right
        graph_pos += 1

    #################################################
    # pos is passed by value, original pos
    # still at 1
    # move input labels tape to right until blank
    while labels_tape[labels_pos] != '_':
        labels_pos -= 1
    labels_pos += 1

    # move input graph tape to right until blank
    graph_pos -= 1
    while graph_tape[graph_pos] != '_':
        graph_pos -= 1
    graph_pos += 1

def initialize_permutation_tapes(
        permutation_tape_temp, permutation_tape_temp_pos,
        labels_tape, labels_pos, 
        permutation_tape1, permutation_tape1_pos,
        permutation_tape2, permutation_tape2_pos
):
    # initialize permutation1 tape
    # label tape is used to keep count
    permutation_tape_temp[permutation_tape_temp_pos] = labels_tape[labels_pos]
    while True:

        # move label tape left to beginning
        while labels_tape[labels_pos] != '_':
            labels_pos -= 1
        labels_pos += 1

        while True:
            # to keep count
            if labels_tape[labels_pos] == '_':
                labels_pos -= 1
                break
            
            else:
                permutation_tape1[permutation_tape1_pos] = permutation_tape_temp[permutation_tape_temp_pos]
                permutation_tape1_pos += 1
                labels_pos += 1
        
        # move left until input labels has encountered the same label as the temp permutation
        while labels_tape[labels_pos] != permutation_tape_temp[permutation_tape_temp_pos]:
            labels_pos -= 1
        labels_pos += 1 # moves the label tape to the next character

        if labels_tape[labels_pos] == '_':
            break
        
        # set permutation tape to next label in label tape
        permutation_tape_temp[permutation_tape_temp_pos] = labels_tape[labels_pos]

    #initialize permutation2 tape for graph
    # move input label tape left
    labels_pos -= 1
    while labels_tape[labels_pos] != '_':
        labels_pos -= 1
    labels_pos += 1

    # move input permutation 1 to right
    permutation_tape1_pos -= 1
    while permutation_tape1[permutation_tape1_pos] != '_':
        permutation_tape1_pos -= 1
    permutation_tape1_pos += 1

    while True:
        permutation_tape2[permutation_tape2_pos] = labels_tape[labels_pos]
        permutation_tape2_pos += 1
        permutation_tape1_pos += 1 # for counting length of permutation 2 tape
        labels_pos += 1

        if labels_tape[labels_pos] == '_':
            # move input label tape left
            labels_pos -= 1
            while labels_tape[labels_pos] != '_':
                labels_pos -= 1
            labels_pos += 1
        
        if permutation_tape1[permutation_tape1_pos] == '_':
            break

    ###################################################
    # pos is still at 1 (passed by value)
    # move input permutation 1 left
    permutation_tape1_pos -= 1
    while permutation_tape1[permutation_tape1_pos] != '_':
        permutation_tape1_pos -= 1
    permutation_tape1_pos += 1

    # move input permutation 2 left
    permutation_tape2_pos -= 1
    while permutation_tape2[permutation_tape2_pos] != '_':
        permutation_tape2_pos -= 1
    permutation_tape2_pos += 1

def initialize_graphs_tape(
    graph_tape, graph_pos,
    temp_conn_tape, temp_conn_tape_pos
):

    # for each graph in graph
    while True:
        if graph_tape[graph_pos] == '_':
            break

        if graph_tape[graph_pos] == '|':

            # move tape head to left of | 
            graph_pos -= 1
            temp_conn_tape[temp_conn_tape_pos] = graph_tape[graph_pos]
            graph_pos += 2 # move tape head to right of | 
            temp_conn_tape_pos += 1

            temp_conn_tape[temp_conn_tape_pos] = graph_tape[graph_pos]
            temp_conn_tape_pos += 1
            temp_conn_tape[temp_conn_tape_pos] = '|'
            temp_conn_tape_pos += 1
        
        graph_pos += 1
    
    return graph_pos, temp_conn_tape_pos

def create_adjacency_matrix(
    graph_tape, graph_tape_pos,
    adjacency_matrix_tape, adjacency_matrix_tape_pos,
    permutation1_tape_pos,
    permutation1_tape, permutation2_tape,
    boolean_tape, boolean_tape_pos
):
    # initalize adjacency list to zeros, using permutation tape 1
    # to get sense of length
    while permutation1_tape[permutation1_tape_pos] != '_':
        adjacency_matrix_tape[adjacency_matrix_tape_pos] = '0'
        permutation1_tape_pos += 1
        adjacency_matrix_tape_pos += 1
    
    permutation1_tape_pos = 1
    adjacency_matrix_tape_pos = 1

    while True: 
        # if reached end of graph tape
        if graph_tape[graph_tape_pos] == '_':
            break

        if graph_tape[graph_tape_pos] == '|':
            permutation1_tape_pos = 1
            adjacency_matrix_tape_pos = 1

            while True:
                # write zeros to boolean tape
                boolean_tape[boolean_tape_pos] = '0'
                boolean_tape_pos += 1
                boolean_tape[boolean_tape_pos] = '0'
                boolean_tape_pos -= 1

                # move graph tape back one
                graph_tape_pos -= 1
                
                # if label of left is equal to the label in permutation 1, write 1
                # to boolean tape
                if graph_tape[graph_tape_pos] == permutation1_tape[permutation1_tape_pos]:
                    boolean_tape[boolean_tape_pos] = '1'
                else:
                    boolean_tape[boolean_tape_pos] = '0'

                boolean_tape_pos += 1 # move boolean tape right
                graph_tape_pos += 2 # move to right label

                # if label of right is equal to the label in permutation 2, write 1
                # to boolean tape
                if graph_tape[graph_tape_pos] == permutation2_tape[permutation1_tape_pos]:
                    boolean_tape[boolean_tape_pos] = '1'
                else:
                    boolean_tape[boolean_tape_pos] = '0'
                boolean_tape_pos = 1 # move boolean tape to start

                # check if boolean tape only has 1s
                # if yes, write 1 to the adjacency matrix tape,
                # otherwise ignore
                if boolean_tape[boolean_tape_pos] == '1':
                    boolean_tape_pos += 1
                    if boolean_tape[boolean_tape_pos] == '1':
                        adjacency_matrix_tape[adjacency_matrix_tape_pos] = '1'
                    else:
                        pass
                else:
                    pass
                
                # reset boolean tape to beginning
                boolean_tape_pos = 1
                
                # move to next permutation
                permutation1_tape_pos += 1
                adjacency_matrix_tape_pos += 1
                
                # if reach end of all permutations
                if permutation1_tape[permutation1_tape_pos] == '_':
                    break

                graph_tape_pos -= 1
            
            # move graph tape onto the | char, which will be
            # move right again
            graph_tape_pos += 1

        # move graph tape right
        graph_tape_pos += 1

def initalize_graph_connection_values(
    conn_value_tape, conn_value_pos,
    graph_tape, graph_pos, permut1_pos,
    permut1_tape, permut2_tape,
    boolean_tape, boolean_pos
):
    # all pos variables are assumed to be initialized at 1

    # loop each connection in graph
    while True:

        # initialize boolean tape to zero
        boolean_tape[boolean_pos] = '0'
        boolean_pos += 1
        boolean_tape[boolean_pos] = '0'
        boolean_pos -= 1

        # loop through the permutations until both boolean char are '1'
        graph_pos += 1
        while True:

            # until it sees '|'
            while graph_tape[graph_pos] != '|':
                graph_pos += 1

            # move graph tape to label for permut1
            graph_pos -= 1

            # check if label in permut1 matches 
            permut1_matches_graph_label = graph_tape[graph_pos] == permut1_tape[permut1_pos]
            if permut1_matches_graph_label:
                boolean_tape[boolean_pos] = '1'
            else:
                boolean_tape[boolean_pos] = '0'
            boolean_pos += 1

            # move graph tape to left of '|' char
            graph_pos += 2
            permut2_matches_graph_label = graph_tape[graph_pos] == permut2_tape[permut1_pos]
            if permut2_matches_graph_label:
                boolean_tape[boolean_pos] = '1'
            else:
                boolean_tape[boolean_pos] = '0'
            
            # move boolean pos back to beginning
            boolean_pos -= 1

            # check if both char in boolean tape are '1's
            graph_pos += 2
            if boolean_tape[boolean_pos] == '1':
                boolean_pos += 1
                # if both boolean variables are '1's
                if boolean_tape[boolean_pos] == '1':
                    # move graph tape to right on the connection value
                    # past the ':' char, and exit the permutation tape
                    boolean_pos -= 1
                    conn_value_tape[conn_value_pos] = graph_tape[graph_pos]
                    break

                else:
                    boolean_pos -= 1
            else:
                pass
            
            conn_head_reads_empty = conn_value_tape[conn_value_pos] == '_'
            if conn_head_reads_empty:
                conn_value_tape[conn_value_pos] = '#'

            # move permutation pos to the next labels on permut1 and permut2
            permut1_pos += 1
            conn_value_pos += 1

            # exit if reached the end of the permutation tapes
            if permut1_tape[permut1_pos] == '_' and permut2_tape[permut1_pos] == '_':
                break

            # code below executes if both boolean tape contains zeros
            # move graph tape to left on the '|' char
            graph_pos -= 3
        
        # reset permutation tape heads to beginning
        permut1_pos = 1
        conn_value_pos = 1

        graph_pos += 1
        if graph_tape[graph_pos] == '_':
            break

def initialize_sub_labels_tape(
    main_labels_tape, main_labels_pos, # whole graph to select random labels from
    input_labels_tape, input_labels_pos, # for determining the length of sub graph
    sub_labels_tape, sub_labels_pos,
):

    # loop through main labels
    # allowed to reselect the same labels for simplicity
    main_labels_pos += 1
    while True:

        if random.randint(0, 1) == 1: # randomly select the label
            sub_labels_tape[sub_labels_pos] = main_labels_tape[main_labels_pos]

            sub_labels_pos += 1
            input_labels_pos += 1
            # check if sub labels has reached the length of the input labels
            if (sub_labels_tape[sub_labels_pos] == '_' and
                input_labels_tape[input_labels_pos] == '_'):
                break # stop looping and exit function

            else:
                pass

        else:
            pass

        main_labels_pos += 1

        # move main labels tape back to beginning
        # if not enough sub labels have been selected
        if main_labels_tape[main_labels_pos] == '_':
            main_labels_pos -= 1
            while main_labels_tape[main_labels_pos] != '_':
                main_labels_pos -= 1
            main_labels_pos += 1

def compare_adjacency_matrices(
    adj_matx1, adj_matx1_pos,
    adj_matx2, adj_matx2_pos,
    conn1_tape, conn1_pos,
    conn2_tape, conn2_pos,
    boolean_tape, boolean_tape_pos
):

    # initialize boolean tape to true
    boolean_tape[boolean_tape_pos] = '1'

    while True:
        # check if adjacency matrics are the same
        if adj_matx1[adj_matx1_pos] == '_' and adj_matx2[adj_matx2_pos] == '_':
            break
        elif adj_matx1[adj_matx1_pos] == adj_matx2[adj_matx2_pos]:
            pass
        else:
            boolean_tape[boolean_tape_pos] = '0'
            break
        
        # check if connection values are the same
        if (conn1_tape[conn1_pos] == conn2_tape[conn2_pos] or 

            # mitigates bug when connection value for input graph is missing
            # a hashtag
           (conn1_tape[conn1_pos] == '_' and conn2_tape[conn2_pos] == '#')):
            pass

        else:
            boolean_tape[boolean_tape_pos] = '0'

        adj_matx1_pos += 1
        adj_matx2_pos += 1
        conn1_pos += 1
        conn2_pos += 1
    
def reset_tape(
    tape, pos
):
    # move to end of tape
    pos += 1
    while tape[pos] != '_':
        pos += 1
    pos -= 1

    # reset to _ until beginning
    while tape[pos] != '_':
        tape[pos] = '_'
        pos -= 1

def copy_subgraph_to_result(
    sub_matrix, sub_matrix_pos,
    permutation1, permutation1_pos,
    permutation2, permutation2_pos,
    matching_graph_tape, matching_graph_tape_pos
):
    
    while True:
        if sub_matrix[sub_matrix_pos] == '_':
            break

        elif sub_matrix[sub_matrix_pos] == '1':
            matching_graph_tape[matching_graph_tape_pos] = permutation1[permutation1_pos]
            matching_graph_tape_pos += 1
            matching_graph_tape[matching_graph_tape_pos] = permutation2[permutation2_pos]
            matching_graph_tape_pos += 1
            matching_graph_tape[matching_graph_tape_pos] = ','
            matching_graph_tape_pos += 1
        
        elif sub_matrix[sub_matrix_pos] == '0':
            pass

        sub_matrix_pos += 1
        permutation1_pos += 1
        permutation2_pos += 1
    
    matching_graph_tape[matching_graph_tape_pos] = '#'
    matching_graph_tape_pos += 1

    return matching_graph_tape_pos
