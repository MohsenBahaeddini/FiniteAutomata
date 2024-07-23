import graphviz
from graphviz import Digraph
from PySimpleAutomata import automata_IO, NFA, DFA
from graphviz import Digraph
from collections import deque

# Helper function to generate power set of a set
def power_set(s):
    """Generate the power set of the input set s."""
    # Start with just the empty set
    p_set = [set()]
    for elem in s:
        # For every element in the original set, add it to the existing subsets
        # to create new subsets.
        new_subsets = [subset.union({elem}) for subset in p_set]
        p_set.extend(new_subsets)
    return p_set

# Define the NFA transition function
nfa = {
    'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
    'q1': {'0': set(), '1': {'q2'}},
    'q2': {'0': set(), '1': set()}
}

# NFA's start state and final states
start_state = 'q0'
final_states = {'q2'}

# Generate all possible DFA states
dfa_states = list(map(set, power_set(nfa.keys())))

# Initialize the DFA transition table
dfa_transition_table = {}

# Function to get the closure of a set of states for a given input
def get_closure(states, input):
    closure = set()
    for state in states:
        closure |= nfa.get(state, {}).get(input, set())
    return closure

# Build the DFA transition table
for state in dfa_states:
    state_str = frozenset(state)  # Use frozenset to have a hashable type for dictionary keys
    dfa_transition_table[state_str] = {}
    for input in ['0', '1']:
        closure = get_closure(state, input)
        dfa_transition_table[state_str][input] = frozenset(closure)

# Display the full DFA transition table
print("       State         |          0           |          1")
print("---------------------------------------------------------------")
for state, transitions in dfa_transition_table.items():
    print(
        "{star} {state:15} | {zero:15} | {one:15}".format(
            star='*' if final_states.intersection(state) else ' ',
            state=str(set(state)).ljust(15),
            zero=str(set(transitions['0'])).ljust(15),
            one=str(set(transitions['1'])).ljust(15)
        )
    )

# Identify reachable states for L(A) = L(B)
reachable_states = set()
queue = [frozenset([start_state])]

while queue:
    current = queue.pop(0)
    reachable_states.add(current)
    for symbol in ['0', '1']:
        next_state = dfa_transition_table[current][symbol]
        if next_state and next_state not in reachable_states:
            queue.append(next_state)

# Convert states to string representation for graphviz
# Update the state labels to remove quotation marks
state_strs = {state: '{' + ', '.join(state) + '}' for state in reachable_states}

# Reinitialize the DFA diagram to apply the changes
dfa_diagram = Digraph('DFA')
dfa_diagram.attr(rankdir='LR', size='8,5')

# Add states and transitions to the diagram 
for state in reachable_states:
    label = state_strs[state]
    if state.intersection(final_states):
        dfa_diagram.node(label, label, shape='doublecircle')
    else:
        dfa_diagram.node(label, label, shape='circle')

    for input_symbol in ['0', '1']:
        next_state = dfa_transition_table[state][input_symbol]
        if next_state in reachable_states:
            next_state_label = state_strs[next_state]
            dfa_diagram.edge(label, next_state_label, label=input_symbol)

# Add a solid arrow for the initial state 
dfa_diagram.attr('node', shape='plaintext')
dfa_diagram.node('start', label='')
dfa_diagram.edge('start', state_strs[frozenset([start_state])], label='', style='solid')

# Re-render and save the diagram with the corrected labels
unquoted_diagram_filename = 'V9_dfa_diagram'
dfa_diagram.render(unquoted_diagram_filename, format='png', cleanup=True)

# Provide path to the saved diagram
unquoted_diagram_path = f"{unquoted_diagram_filename}.png"
unquoted_diagram_path