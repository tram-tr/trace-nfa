#!/usr/bin/env python3
import time
import sys
import csv
from tqdm import tqdm

# read nfa file
def read_NFA(file_name):
    global NFA # name of the machine
    global Q # states name
    global symbols # characters
    global start # start state
    global accept # list of accept states
    global T # transitions
    T = {}
    with open(file_name) as file:
        for index, line in tqdm(enumerate(file), desc='Reading NFA file...'):
            if index == 0:
                NFA = line.rstrip().split(',')[0]
            elif index == 1:
                Q = list(filter(None, line.rstrip().split(',')))
            elif index == 2:
                symbols = list(filter(None, line.rstrip().split(',')))
            elif index == 3:
                start = line.rstrip().split(',')[0]
            elif index == 4:
                accept = list(filter(None, line.rstrip().split(',')))
            else:
                read_transition(line.rstrip())

# create dictionary for transitions
def read_transition(transition):
    curr, input, next = transition.split(',')[0:3]
    curr = curr
    next = next
    if curr not in T:
        T[curr] = []
    T[curr].append((input, next))
    
# trace all paths of nfa
def trace(string):
    # triples = (curr, curr_string, epsilon)
    # curr = current state
    # curr_string = current input string
    # epsilon = True if the current state accepts epsilon
    
    frontier = [(start, string, False, start)] # stack
    paths = 0
    accept_paths = 0
    accept_seq = []
    # empty string
    if (string == '~$'):
        if (start[0] == '*' or start in accept):
            accept_paths += 1
            paths += 1
            accept_seq.append(start)

    while frontier:
        curr, curr_string, epsilon, seq = frontier.pop()
        if (curr_string == '$'):
            if (curr[0] == '*' or curr in accept):
                accept_paths += 1
                curr_string = '~$'
                accept_seq.append(seq)

            if (not epsilon):
                paths += 1

        for next in T[curr]:
            if (next[0] == '~'):
                frontier.append((next[1], curr_string, True, seq + ',' + next[1]))   
            if (curr_string[0] == next[0]):
                frontier.append((next[1], curr_string[1:], False, seq + ',' + next[1]))
   
    return paths, accept_paths, accept_seq

# write output
def write_output(input_file, input_string, paths, accept_paths, accept_seq):
    output_file = input_file[:-4] + '-' + input_string + '-output.csv'
    with open(output_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['input_file','NFA_name','input_string','possible_paths', 'accept_paths'])
        writer.writerow([input_file, NFA, input_string, paths, accept_paths])
        for seq in accept_seq:
            writer.writerow(seq.split(','))

def main():
    file = input('Enter NFA file name: ')
    read_NFA(file)
    input_string = input('Input a string: ')
    input_string += '$' #indicate end of string
    paths, accept_paths, accept_seq = trace(input_string)
    print(paths, accept_paths)
    for seq in accept_seq:
        print(seq)
    write_output(file, input_string[:-1], paths, accept_paths, accept_seq)

if __name__ == '__main__':
    main()