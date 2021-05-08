#!/usr/bin/env python
#-*- coding:utf-8 -*-
from Verifier4UP.src.CEGAR.DFA import DFA, cross_product
from Verifier4UP.src.Parser.color import red_none
# ----------------------------------------------------- auxiliary func ---------------------------------------- #
# translate ats into automata
def trans_fsm(ats):
    ats_lst = ats.split("\n")
    for line in ats_lst:
        if "states" in line:
            states = line[line.find("{") + 1:line.rfind("}")].split(" ")
            states.append("--")     # add new state
        if "initialStates" in line:
            start = line[line.find("{") + 1:line.rfind("}")]
        if "finalStates" in line:
            accepts = [line[line.find("{") + 1:line.rfind("}")]]
            break
        if "alphabet" in line:
            alphabet = line[line.find("{") + 1:line.rfind("}")].split(" ")

    def delta(state, char):
        for line in ats_lst:
            if ("(" + state + " " + char) in line:
                return line[line.rfind("q"): line.rfind(")")]
        return "--"     # undefined transition is targeted to state "--"
    fsm = DFA(states=states, start=start, accepts=accepts, alphabet=alphabet, delta=delta)
    return fsm

# present automata
def fsm_show(fsm):
    print("This DFA has %s states" % len(fsm.states))
    print("States:", fsm.states)
    print("Alphabet:", fsm.alphabet)
    print("Starting state:", fsm.start)
    print("Accepting states:", fsm.accepts)
    print("Transition function:")
    result = " \t"
    for state in fsm.states:
        result = result + str(state) + "\t"
    print(result)
    for c in fsm.alphabet:
        result = c + "\t"
        for state in fsm.states:
            next_state = fsm.delta(state, c)
            if next_state in fsm.accepts:
                next_state = str(next_state)
                next_state = red_none%next_state
            else:
                next_state = str(next_state)
            result = result + next_state + "\t"
        print(result)
    print("Current state:", fsm.current_state)
    print("Currently accepting:", fsm.status())
    print("")

# automata's emptiness checking
def check_empty(fsm):
    init_state = fsm.start          # initail state
    accept_state = fsm.accepts      # accepted state
    reachable_state_from_init = fsm.reachable_from(init_state)
    for state in accept_state:
        if state in reachable_state_from_init:
            return "false", find_reachable_trace(fsm, init_state, accept_state)
    return "true", ''

# get a accepted word from automata
def find_reachable_trace(fsm, init_state, accept_state):
    delta = fsm.delta           # transition
    alphabet = fsm.alphabet     #  alphabet - the first parameters of func
    work_list = [""]                # to be checked word
    last_state = {"": init_state}   # to be checked word's last state
    while True:
        # for word in work_list:
        #     print(word)
        # print("------------------\n")
        new_work_list = []      # do a further step and get a new word (BFS)
        new_last_state = {}     # corresponded word's last state
        for word in work_list:
            state = last_state[word]
            for action in alphabet:
                next_state = delta(state, action)
                if next_state in accept_state:
                    return word + action
                else:
                    if check_valid_state(next_state, alphabet, delta):
                        new_word = word + action + " "
                        new_work_list.append(new_word)
                        new_last_state[new_word] = next_state
        work_list = new_work_list
        last_state = new_last_state

# check if the state is valid
def check_valid_state(state, alphabet, delta):
    valid_flag = False
    for action in alphabet:
        if state != delta(state, action):
            valid_flag = True
            break
    return valid_flag
    # if type(state) == str:
    #     if state == "--":
    #         return False
    #     else:
    #         return True
    # elif isinstance(state[0], str):   # ('q1', '--')
    #     if state[0] == '--':
    #         return False
    #     else:
    #         return True
    # else:                   # (('q1', '--'), '--')
    #     state = state[0]
    #     return check_valid_state(state)


# translating the alphabet sequence into the statement sequence
def translate_albet_to_stat_save(dir, alphabet_seq, entry_point, exit_point):

    reverse_dir = {}
    for key in dir.keys():
        reverse_dir[dir[key]] = key

    word = alphabet_seq.split(" ")
    trace = ""
    for i in word:
        if reverse_dir[i] in entry_point:
            trace = trace + reverse_dir[i] + "; -Entry\n"
        elif reverse_dir[i] in exit_point:
            trace = trace + reverse_dir[i] + "; -Exit\n"
        else:
            trace = trace + reverse_dir[i] + ";\n"

    return trace


def translate_albet_to_stat_print(dir, alphabet_seq):

    reverse_dir = {}
    for key in dir.keys():
        reverse_dir[dir[key]] = key

    trace = ""
    word = alphabet_seq.split(" ")
    for i in word:
        trace += reverse_dir[i] + "; "
    return trace[:-2]


# ----------------------------------------------------- other func ---------------------------------------- #
# D1/D2
def fsm_difference(D1, D2):
    """Constructs an unminimized DFA recognizing the difference of the languages of two given DFAs."""
    def f(a, b):
        if a == True and b == False:
            return True
        else:
            return False
    return cross_product(D1, D2, f)


if __name__ == "__main__":
   pass