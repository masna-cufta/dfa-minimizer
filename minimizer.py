import sys
from collections import deque

def parse_input():  
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

def remove_unreachable_states(states, alphabet, accept_states, start_state, transitions):
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

    new_states = [s for s in states if s in reachable]
    new_accept_states = [s for s in accept_states if s in reachable]
    new_transitions = {s: transitions[s] for s in new_states}

    return new_states, new_accept_states, new_transitions

def minimize_dfa(states, alphabet, accept_states, start_state, transitions):
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
                    example = subgroup[0]
                    same = True
                    for symbol in alphabet:
                        target1 = transitions[state][symbol]
                        target2 = transitions[example][symbol]

                        group_for_target1 = None
                        group_for_target2 = None
                        for g in groups:
                            if target1 in g:
                                group_for_target1 = g
                            if target2 in g:
                                group_for_target2 = g

                        if group_for_target1 != group_for_target2:
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

    replacements = {}
    for group in groups:
        representative = min(group)
        for s in group:
            replacements[s] = representative

    new_states_set = set(replacements.values())
    new_states = sorted(new_states_set)

    new_accept_set = {replacements[s] for s in accept_states}
    new_accept_states = sorted(new_accept_set)

    new_start_state = replacements[start_state]

    new_transitions = {}
    for state in new_states:
        new_transitions[state] = {}
        for symbol in alphabet:
            old_target = None
            for s in transitions:
                if replacements[s] == state:
                    old_target = transitions[s][symbol]
                    break
            new_transitions[state][symbol] = replacements[old_target]

    return new_states, alphabet, new_accept_states, new_start_state, new_transitions

def main():
    states, alphabet, accept_states, start_state, transitions = parse_input()

    states, accept_states, transitions = remove_unreachable_states(states, alphabet, accept_states, start_state, transitions)

    states, alphabet, accept_states, start_state, transitions = minimize_dfa(states, alphabet, accept_states, start_state, transitions)

    print(','.join(states))
    print(','.join(alphabet))
    print(','.join(accept_states))
    print(start_state)
    for state in states:
        for symbol in alphabet:
            dest = transitions[state][symbol]
            line = state + "," + symbol + "->" + dest
            print(line)

if __name__ == '__main__':
    main()
