# DFA Minimizer (Python)

This program minimizes a deterministic finite automaton (DFA) by removing unreachable states and merging equivalent states using partition refinement.

## Input Format

The program reads input from standard input in the following format:

1. Comma-separated list of states  
2. Comma-separated list of input symbols (alphabet)  
3. Comma-separated list of accepting (final) states  
4. Start state  
5. Transition rules in the format:  
   state,input_symbol->next_state

Example:

q0,q1,q2,q3,q4  
0,1  
q4  
q0  
q0,0->q1  
q0,1->q2  
q1,0->q0  
q1,1->q3  
q2,0->q4  
q2,1->q0  
q3,0->q4  
q3,1->q1  
q4,0->q4  
q4,1->q4

## How to Run

Save your input in a file called `input.txt`, then run:

python3 minimizer.py < input.txt

## Output Format

The minimized DFA is printed in the same format:

1. Comma-separated list of minimized states  
2. Comma-separated alphabet  
3. Comma-separated accepting states  
4. Start state  
5. Transitions in the format:  
   state,input_symbol->next_state

## No Dependencies

Only uses Python standard libraries. Compatible with Python 3.x.
