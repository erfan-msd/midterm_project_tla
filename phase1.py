import json
from queue import Queue

def read_json_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def write_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

class NFA:
    def __init__(self, data):
        self.states = set(data['states'])
        self.input_symbols = set(data['input_symbols'])
        self.transitions = data['transitions']
        self.initial_state = data['initial_state']
        self.final_states = set(data['final_states'])
        
    def get_next_states(self, state, symbol):
        if (state, symbol) in self.transitions:
            return set(self.transitions[(state, symbol)])
        else:
            return set()

class DFA:
    def __init__(self, input_symbols):
        self.states = set()
        self.start_state = set()
        self.final_states = set()
        self.transitions = {}
        self.input_symbols = input_symbols
        
    def add_state(self, state):
        self.states.add(state)
        self.transitions[state] = {}
        
    def add_transition(self, from_state, symbol, to_state):
        self.transitions[from_state][symbol] = to_state
        
    def get_next_state(self, state, symbol):
        return self.transitions[state][symbol]
    
    def to_dict(self):
        return {
            'states': list(self.states),
            'input_symbols': list(self.input_symbols),
            'transitions': self.transitions,
            'initial_state': list(self.start_state)[0],
            'final_states': list(self.final_states)
        }

def nfa_to_dfa(nfa):
    dfa = DFA(nfa.input_symbols)
    initial_set = {nfa.initial_state}
    dfa.start_state = initial_set
    state_sets = {}
    queue = Queue()
    queue.put(initial_set)
    while not queue.empty():
        current_set = queue.get()
        state_sets[frozenset(current_set)] = current_set
        for symbol in nfa.input_symbols:
            next_set = set()
            for state in current_set:
                next_set |= nfa.get_next_states(state, symbol)
            if len(next_set) > 0:
                if frozenset(next_set) not in state_sets:
                    dfa.add_state(frozenset(next_set))
                    queue.put(next_set)
                dfa.add_transition(frozenset(current_set), symbol, frozenset(next_set))
    for state_set in state_sets.values():
        if nfa.final_states.intersection(state_set):
            dfa.final_states.add(frozenset(state_set))
    return dfa

nfa_data = read_json_file('input1.json')
nfa = NFA(nfa_data)
dfa = nfa_to_dfa(nfa)
dfa_data = dfa.to_dict()
write_json_file('output1.json', dfa_data)
