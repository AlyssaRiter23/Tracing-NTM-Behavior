from collections import deque
import argparse

# define a tree node to represent each configuration
class configuration:
    def __init__(self, state, tape, head_position, depth, parent=None):
        self.state = state
        self.tape = tape
        self.head_position = head_position
        self.depth = depth
        self.parent = parent

# function to simulate a NTM using breadth first search
def turing_machine_bfs(machine, input_string, max_depth=None, max_transitions=None, debug_flag=False):
    file = open("output.txt", "a") # open output file for writing
    ## parse the machine configuration ##
    if len(input_string) == 0:
        tape = list(input_string) + ['_'] # ensure there is a blank space to signify the end of the input string
    else:
        tape = list(input_string)
    # define the transitions
    transitions = machine["transitions"]
    explored_paths = []  # to record the explored tree
    transition_count = 0 # count the number of transitions that occur
    configuration_count = 0 # count the number of configurations
    ## initialize the root node -> aka the starting configuration ##
    root = configuration(machine["start_state"], tape, 0, 0)
    queue = deque([root]) # create a queue that is accessible from the front and back of the configurations
    # print out the input string
    print(f"Input string: {input_string}")
    file.write(f"\nInput string: {input_string}\n")
    while queue:
        # pop the next configuration to explore
        current_node = queue.popleft()
        configuration_count += 1
        # get the new configuration features (state, tape, head position, and search depth)
        current_state = current_node.state
        current_tape = current_node.tape
        head_position = current_node.head_position
        depth = current_node.depth

        # update the explored paths tree
        if len(explored_paths) <= depth:
            explored_paths.append([])
        # add the configuration to the explored_paths -> current tape before the head, current state, tape at the head and beyond
        explored_paths[depth].append([
            "".join(current_tape[:head_position]),
            current_state,
            "".join(current_tape[head_position:])
        ])

        # used for debugging
        if debug_flag:
            print(f"state: {current_state}, tape: {''.join(current_tape)}, head pos: {head_position}, depth: {depth}")

        machine_name = machine["machine_name"] # define machine name for printing purposes
        # check for acceptance or rejection
        if current_state == machine["accept_state"]: # if in accept state halt and display stats to stdout & file
            print(f"Machine Name: {machine_name}")
            file.write(f"Machine Name: {machine_name}")
            print(f"String accepted in {transition_count+1} transitions.")
            file.write(f"\nString accepted in {transition_count+1} transitions.")
            print(f"Depth of tree: {depth}")
            file.write(f"\nDepth of tree: {depth}")
            print(f"Configurations explored: {configuration_count}")  # Print explored configurations
            file.write(f"\nConfigurations explored: {configuration_count}")
            print("\nExplored Paths Tree:")
            file.write(f"\nExplored Paths Tree:")
            print_tree(explored_paths, file)
            return
        
        # check to ensure maximum depth is not exceeded -> prevents simulation from running to long
        if max_depth is not None and depth >= max_depth:
            print(f"Machine Name: {machine_name}")
            file.write(f"\nMachine Name: {machine_name}")
            print(f"Execution stopped after reaching max depth of {max_depth}.")
            file.write(f"\nExecution stopped after reaching max depth of {max_depth}")
            print(f"Configurations explored: {configuration_count}")  # Print explored configurations
            file.write(f"\nConfigurations explored: {configuration_count}")
            print("\nExplored Paths Tree:")
            file.write(f"\nExplored Paths Tree:")
            print_tree(explored_paths, file)
            return
        # check to ensure that the maximium number of transitions is not exceeded
        if max_transitions is not None and transition_count >= max_transitions:
            print(f"Machine Name: {machine_name}")
            file.write(f"Machine Name: {machine_name}")
            print(f"Execution stopped after {transition_count+1} transitions.")
            file.write(f"Execution stopped after {transition_count+1} transitions.")
            print(f"Depth of tree: {depth}")
            file.write(f"\nDepth of tree: {depth}")
            print(f"Configurations explored: {configuration_count}")  # Print explored configurations
            file.write(f"\nConfigurations explored: {configuration_count}")
            print("\nExplored Paths Tree:")
            file.write("\nExplored Paths Tree:")
            print_tree(explored_paths, file)
            return

        # create other configurations based on next transition
        for transition in transitions:
            # set the configuration specs
            from_state, read_symbol, next_state, write_symbol, direction = transition

            # apply the transition if it matches the current configuration
            if from_state == current_state and read_symbol == current_tape[head_position]:
                new_tape = current_tape[:]  # copies the tape
                new_tape[head_position] = write_symbol # update the symbol

                # move the tape head to the right or left base on configuration direction
                if direction == 'R':
                    new_head_position = head_position + 1
                elif direction == 'L':
                    new_head_position = head_position - 1

                # if the head position moves too far left add a blank & reset head position
                if new_head_position < 0:
                    new_tape.insert(0, '_')
                    new_head_position = 0
                elif new_head_position >= len(new_tape):
                    new_tape.append('_')

                # create a new child configuration and add it to the queue -> increase the depth of the tree by 1
                child_node = configuration(
                    next_state, new_tape, new_head_position, depth + 1, current_node
                )
                queue.append(child_node)

                transition_count += 1

    # if the queue is empty and input is not accepted
    print(f"Machine Name: {machine_name}")
    file.write(f"Machine Name: {machine_name}")
    print(f"Input rejected in {transition_count+1} steps.")
    file.write(f"\nInput rejected in {transition_count+1} steps")
    print(f"Depth of tree: {depth}")
    file.write(f"\nDepth of tree: {depth}")
    print(f"Configurations explored: {configuration_count}")  # Print explored configurations
    file.write(f"\nConfigurations explored: {configuration_count}")
    print("\nExplored Paths Tree:")
    file.write("\nExplored Paths Tree:")
    print_tree(explored_paths, file)


# function to parse the csv file
def parse_file(file_path):
    with open(file_path, 'r') as file:
        machine_name = file.readline().strip()
        state_names = file.readline().strip().split(',')
        sigma = file.readline().strip().split(',')
        gamma = file.readline().strip().split(',')
        start_state = file.readline().strip()
        accept_state = file.readline().strip()
        reject_state = file.readline().strip()

        transitions = []
        for line in file:
            if line.strip():
                transitions.append(tuple(line.strip().split(',')))
    # return a dictionary of the TM tuple definition
    return {
        "machine_name": machine_name,
        "states": [state.strip() for state in state_names],
        "input_alphabet": [symbol.strip() for symbol in sigma],
        "tape_alphabet": [symbol.strip() for symbol in gamma],
        "start_state": start_state,
        "accept_state": accept_state,
        "reject_state": reject_state,
        "transitions": transitions,
    }

# function to print the explored paths tree
def print_tree(tree, file):
    for level, paths in enumerate(tree):
        print(f"Level {level:<2}: {paths}")
        file.write(f"\nLevel {level:<2}: {paths}")

# test the function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a Turing Machine.")
    parser.add_argument("-f", "--file", required=True, help="Path to the file describing the machine.")
    parser.add_argument("-i", "--input", required=True, help="Input string to run on the machine.")
    parser.add_argument("-d", "--max_depth", type=int, default=None, help="Maximum depth of the configuration tree.")
    parser.add_argument("-t", "--max_transitions", type=int, default=None, help="Maximum number of transitions.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for detailed tracing.")
    args = parser.parse_args()

    machine = parse_file(args.file)
    turing_machine_bfs(machine, args.input, args.max_depth, args.max_transitions, args.debug)
