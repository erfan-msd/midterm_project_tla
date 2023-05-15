import json

def is_accepted(finite_automata, input_string):
    current_state = finite_automata['initial_state']
    for symbol in input_string:
        if symbol not in finite_automata['input_symbols']:
            return False
        current_state = finite_automata['transitions'][current_state].get(symbol, None)
        if current_state is None:
            return False
    return current_state in finite_automata['final_states']

if __name__ == '__main__':
    with open('D:\IUST\Theory_Languages_Machines\Projects\TLA01-Projects-main\TLA01-Projects-main\samples\phase3-sample\in\input1.json', 'r') as f:
        fa = json.load(f)

    input_string = input('Enter a string to check: ')
    if is_accepted(fa, input_string):
        print('Accepted')
    else:
        print('Rejected')
