import sys
from collections import deque

def parseInput(): 
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())

    states = lines[0].split(',')
    alphabet = lines[1].split(',')
    accept_states = lines[2].split(',')
    start_state = lines[3]
    transitions = {}

    for line in lines[4:]:
        if not line:
            continue
        left, right = line.split('->')
        current_state, symbol = left.split(',')
        if current_state not in transitions:
            transitions[current_state] = {}
        transitions[current_state][symbol] = right

    return states, alphabet, accept_states, start_state, transitions

def removeUnreachableStates(states, alphabet, accept_states, start_state, transitions):
    reachable = set()
    queue = deque([start_state])  

    while queue:
        state = queue.popleft()
        if state in reachable:
            continue
        reachable.add(state)
        for symbol in alphabet:
            neighbor = transitions[state][symbol]
            if neighbor not in reachable:
                queue.append(neighbor)

    new_states = []
    for s in states:
        if s in reachable:
            new_states.append(s)

    new_accept_states = []
    for s in accept_states:
        if s in reachable:
            new_accept_states.append(s)

    new_transitions = {}
    for s in new_states:
        new_transitions[s] = transitions[s]

    return new_states, new_accept_states, new_transitions

def minimizeDFA(states, alphabet, accept_states, start_state, transitions):
    groups = []
    group1 = []
    group2 = []

    for s in states:
        if s in accept_states:
            group1.append(s)
        else:
            group2.append(s)

    if group1:
        groups.append(group1)
    if group2:
        groups.append(group2)

    changed = True
    while changed:
        new_groups = []
        changed = False

        for group in groups:
            subgroups = []
            for state in group:
                placed = False
                for subgroup in subgroups:
                    ex = subgroup[0]
                    same = True
                    for symbol in alphabet:
                        dest1 = transitions[state][symbol]
                        dest2 = transitions[ex][symbol]

                        group1_for = None
                        group2_for = None
                        for g in groups:
                            if dest1 in g:
                                group1_for = g
                            if dest2 in g:
                                group2_for = g

                        if group1_for != group2_for:
                            same = False
                            break

                    if same:
                        subgroup.append(state) 
                        placed = True
                        break

                if not placed:
                    subgroups.append([state])

            if len(subgroups) > 1:
                changed = True
            for sg in subgroups:
                new_groups.append(sg)

        groups = new_groups

    mapping = {}
    for group in groups:
        representative = min(group)
        for s in group:
            mapping[s] = representative

    new_states_set = set()
    for s in mapping.values():
        new_states_set.add(s)
    new_states = sorted(new_states_set)

    new_accept_set = set()
    for s in accept_states:
        new_accept_set.add(mapping[s])
    new_accept = sorted(new_accept_set)

    new_start = mapping[start_state]

    new_transitions = {}
    for state in new_states:
        new_transitions[state] = {}
        for symbol in alphabet:
            old_dest = None
            for s in transitions: 
                if mapping[s] == state:
                    old_dest = transitions[s][symbol]
                    break
            new_transitions[state][symbol] = mapping[old_dest]

    return new_states, alphabet, new_accept, new_start, new_transitions

def printDFA(states, alphabet, accept_states, start_state, transitions): 
    print(','.join(states))
    print(','.join(alphabet))
    print(','.join(accept_states))
    print(start_state)
    for state in states:
        for symbol in alphabet:
            dest = transitions[state][symbol]
            line = state + "," + symbol + "->" + dest
            print(line)

def main():
    states, alphabet, accept_states, start_state, transitions = parseInput()
    states, accept_states, transitions = removeUnreachableStates(states, alphabet, accept_states, start_state, transitions)
    states, alphabet, accept_states, start_state, transitions = minimizeDFA(states, alphabet, accept_states, start_state, transitions)
    printDFA(states, alphabet, accept_states, start_state, transitions)

if __name__ == '__main__':
    main()
