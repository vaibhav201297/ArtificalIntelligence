#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: zseliger
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time
from queue import PriorityQueue
from math import log

def get_people(lines):
    people = {}

    for line in lines:
        tokens = line[:-1].split(' ')
        requested_people = tokens[1].split('-')[1:]
        unrequested_people = tokens[2].split(',')
        if tokens[2] == '_':
            unrequested_people = []

        people[tokens[0]] = [requested_people, unrequested_people]

    return people

def get_total_cost(people, groups):
    result = len(groups)*5

    # penalties
    for group in groups:
        for person_name in group:
            # not given requested teammate penalty
            for requested_name in people[person_name][0]:
                if requested_name not in group and requested_name != "xxx" and requested_name != "zzz":
                    result += 3
            # wrong group size penalty
            if len(people[person_name][0])+1 != len(group):
                result += 2
            # given unrequested teammate penalty
            for unrequested_name in people[person_name][1]:
                if unrequested_name in group:
                    result += 10

    return result

def get_score(people, groups, depth):
    num_groups = len(groups)
    num_requested = 0
    num_size = 0
    num_unrequested = 0

    # penalties
    for group in groups:
        for person_name in group:
            # not given requested teammate penalty
            for requested_name in people[person_name][0]:
                if requested_name not in group and requested_name != "xxx" and requested_name != "zzz":
                    num_requested += 1
            # wrong group size penalty
            if len(people[person_name][0])+1 != len(group):
                num_size += 1
            # given unrequested teammate penalty
            for unrequested_name in people[person_name][1]:
                if unrequested_name in group:
                    num_unrequested += 1

    return num_groups**5 + num_requested**3 + num_size**2 + num_unrequested**10 + depth**1.5

def get_groups_str(groups):
    res = ''
    for group in groups:
        res += ''.join(group)+";"
    return res

def get_groups_copy(groups):
    result = []
    for group in groups:
        result.append(group.copy())
    return result

def get_successors(groups, checked_states):
    succ = []
    # new_person_name = get_unassigned_people(people, groups)[0]

    # get first group with less than 3 people
    first_group = -1
    for i in range(len(groups)):
        if len(groups[i]) < 3:
            first_group = i
            break
    if first_group == -1: return succ

    groups_copy = get_groups_copy(groups)
    first_group = groups_copy.pop(first_group)

    # make copies for each group it can be inserted into
    for i in range(len(groups_copy)):
        if len(groups_copy[i]) + len(first_group) <= 3:
            new_succ = get_groups_copy(groups_copy)
            new_succ[i] = new_succ[i]+first_group
            if get_groups_str(new_succ) not in checked_states:
                succ.append(new_succ)
                checked_states[get_groups_str(new_succ)] = True

    return succ

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """

    f = open(input_file, "r")
    people = get_people(f.readlines())
    f.close()

    min_cost = -1 # irrelevant as the first value is set when yielded_solution == False
    yielded_solution = False
    checked_states = {}
    initial_state = []
    for person_name in people.keys():
        initial_state.append([person_name])
    checked_states[get_groups_str(initial_state)] = True
    fringe = PriorityQueue()
    fringe.put((get_total_cost(people, initial_state), 0, initial_state))
    while not fringe.empty():
        curr_state = fringe.get()
        depth = curr_state[1]
        curr_state = curr_state[2]
        curr_cost = get_total_cost(people, curr_state)

        # yield curr_state if it's a goal
        if curr_cost < min_cost or yielded_solution == False:
            yield({"assigned-groups": curr_state, "total-cost": curr_cost})
            min_cost = curr_cost
            yielded_solution = True

        # add successors to fringe
        successors = get_successors(curr_state, checked_states)
        for succ in successors:
            fringe.put((get_score(people, succ, depth+1), depth+1, succ))

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n{}\n".format(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
