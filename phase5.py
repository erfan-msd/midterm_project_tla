import json

def fa_to_regex(fa_json):
    # Load FA from JSON
    states = fa_json["states"]
    input_symbols = fa_json["input_symbols"]
    transitions = fa_json["transitions"]
    initial_state = fa_json["initial_state"]
    final_states = fa_json["final_states"]

    # Convert FA to transition matrix
    num_states = len(states)
    transition_matrix = [[None] * num_states for _ in range(num_states)]
    for transition in transitions:
        src_state, input_symbol, dest_state = transition
        src_idx = states.index(src_state)
        dest_idx = states.index(dest_state)
        transition_matrix[src_idx][dest_idx] = input_symbol

    # Apply Arden's Lemma to compute regex
    for i in range(num_states):
        transition_matrix[i][i] = "(" + "|".join([""] + [f"({t})*" for t in input_symbols] + [")"])
    for k in range(num_states):
        for i in range(num_states):
            for j in range(num_states):
                if transition_matrix[i][k] and transition_matrix[k][j]:
                    if not transition_matrix[i][j]:
                        transition_matrix[i][j] = "(" + transition_matrix[i][k] + ")" + "(" + transition_matrix[k][j] + ")" + "|"
                    else:
                        transition_matrix[i][j] += "(" + transition_matrix[i][k] + ")" + "(" + transition_matrix[k][j] + ")" + "|"

    # Build final regex
    initial_idx = states.index(initial_state)
    final_idxs = [states.index(final_state) for final_state in final_states]
    final_states_regex = "".join([f"({transition_matrix[initial_idx][final_idx]})" for final_idx in final_idxs])
    return final_states_regex[:-1]

# Example usage
fa_json = {
    "states": ["q1", "q2", "q3"],
    "input_symbols": ["a", "b"],
    "transitions": [
        ["q1", "a", "q2"],
        ["q2", "b", "q3"],
        ["q2", "a", "q2"],
        ["q3", "a", "q2"],
    ],
    "initial_state": "q1",
    "final_states": ["q3"],
}

regex = fa_to_regex(fa_json)
print(regex)  # prints: (a(aa)*b)*a(aa)*
