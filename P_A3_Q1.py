import graphviz
from PySimpleAutomata import automata_IO, NFA, DFA
from graphviz import Digraph
from collections import deque
from graphviz import Digraph

# Function to generate a transition diagram for an automaton (DFA or NFA)
def generate_transition_diagram(states, alphabet, transitions, start_state, accepting_states):
    # Initialize a directed graph for the automaton using Graphviz
    dot = Digraph('Automaton', format='png')

    # Loop through each state in the automaton
    for state in states:
        # If the state is an accepting state, use a double circle to represent it
        if state in accepting_states:
            dot.node(state, state, shape='doublecircle')
        else:
            # Otherwise, use a regular circle for non-accepting states
            dot.node(state, state)

    # Loop through each state and its transitions in the transition table
    for state, trans in transitions.items():
        for symbol, next_states in trans.items():
            # Check if the transitions are in NFA format (sets of states) or DFA format (single states)
            if isinstance(next_states, set):
                # For NFA format, iterate through each possible next state
                for next_state in next_states:
                    # Create an edge for each transition
                    dot.edge(state, next_state, label=symbol)
            else:
                # For DFA format, create a single edge for the transition
                dot.edge(state, next_states, label=symbol)

    # Add a non-visible start node and an edge to the actual start state to represent the start state
    dot.node('', '', shape='none')
    dot.edge('', start_state)

    return dot

# Define parameters for an NFA example
states = {'q0', 'q1', 'q2'}
alphabet = {'0', '1'}
transitions_nfa = {
    'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
    'q1': {'0': set(), '1': {'q2'}},
    'q2': {'0': set(), '1': set()}
}
start_state = 'q0'
accepting_states = {'q2'}

# Define parameters for a DFA example
transitions_dfa = {
    'q0': {'0': 'q2', '1': 'q0'},
    'q1': {'0': 'q1', '1': 'q1'},
    'q2': {'0': 'q2', '1': 'q1'}
}
# start_state = 'q0'
# accepting_states = 'q1'

# Generate and save the NFA diagram
diagram_nfa = generate_transition_diagram(states, alphabet, transitions_nfa, start_state, accepting_states)
diagram_nfa.render('transition_diagram_nfa', format='png', cleanup=True)

# Generate and save the DFA diagram
diagram_dfa = generate_transition_diagram(states, alphabet, transitions_dfa, start_state, accepting_states)
diagram_dfa.render('transition_diagram_dfa', format='png', cleanup=True)
