#!/usr/bin/env python
#-*- coding:utf-8 -*-

import copy


# ----------------------------------------------- the simplification of tuples ----------------------------------------------------------- #
def find_never_used_vars(program_sequence):

    never_used_lst = []
    program_sequence = copy.deepcopy(program_sequence)
    previous_program_sequence = []
    while previous_program_sequence != program_sequence:
        previous_program_sequence = copy.deepcopy(program_sequence)
        for i in range(len(program_sequence)):
            statement1 = program_sequence[i]
            if ":=" in statement1:
                suspicious_var = statement1[:statement1.find(":=") - 1]
                never_used_flag = True
                for j in range(i+1, len(program_sequence)):
                    statement2 = program_sequence[j]
                    if "assume" in statement2:
                        left_var = statement2[statement2.find("(") + 1: statement2.rfind("=") - 2]
                        right_var = statement2[statement2.rfind("=") + 2: statement2.find(")")]
                        if suspicious_var == left_var or suspicious_var == right_var:
                            never_used_flag = False
                            break
                    elif "(" in statement2:
                        right_vars = statement2[statement2.find("(") + 1:statement2.find(")")].split(', ')
                        if suspicious_var in right_vars:
                            never_used_flag = False
                            break
                    else:
                        right_var = statement2[statement2.find(":=") + 3:]
                        if suspicious_var == right_var:
                            never_used_flag = False
                            break
                if never_used_flag:
                    never_used_lst.append(suspicious_var)
                    program_sequence.pop(i)
                    break
    return never_used_lst


def simplify_triple(triple, conflict_var):

    Equality_To_be_removed = []
    Disequality_To_be_removed = []
    Function_To_be_removed = []
    # detect the irrelevant info
    for var_tuple in triple.Equality:
        if var_tuple[0] in conflict_var and var_tuple[1] in conflict_var:
            pass
        else:
            Equality_To_be_removed.append(var_tuple)
    for var_tuple in triple.Disequality:
        if var_tuple[0][var_tuple[0].find("[")+1:var_tuple[0].find("]")] in conflict_var and var_tuple[1][var_tuple[1].find("[")+1:var_tuple[1].find("]")] in conflict_var:
            pass
        else:
            Disequality_To_be_removed.append(var_tuple)
    for fun_key in triple.Function.keys():
        fun_vars = fun_key[fun_key.find("(")+1:fun_key.find(")")].split(", ")
        if set(fun_vars).issubset(set(conflict_var)) and triple.Function[fun_key] in conflict_var:
            pass
        else:
            Function_To_be_removed.append(fun_key)
    # delete the irrelevant info
    for item in Equality_To_be_removed:
        triple.Equality.remove(item)
    for item in Disequality_To_be_removed:
        triple.Disequality.remove(item)
    for item in Function_To_be_removed:
        del triple.Function[item]




# ----------------------------------------------- the combination of tuples ------------------------------------------------------- #
def eliminate_ghost(origin_dir, state_map, fsm, dir, program_sequence, loop_flag):
    normal_alphabet = list(origin_dir.values())
    # update alphabet
    To_be_remove = []
    for item in fsm.alphabet:
        if not (item in normal_alphabet):
            To_be_remove.append(item)
    for item in To_be_remove:
        fsm.alphabet.remove(item)

    # update transition
    for state_idx in range(len(fsm.states) - 1, 0, -1):
        statement = program_sequence[state_idx - 1]  # consider the statement before entering the state
        if not (dir[statement] in normal_alphabet):
            fsm.combine_state(state_idx - 1, state_idx, state_map, program_sequence, loop_flag)
    To_be_remove = []
    for trans in fsm.transition:
        if not (trans[1] in normal_alphabet):
            To_be_remove.append(trans)
    for trans in To_be_remove:
        fsm.transition.remove(trans)


# ----------------------------------------------- the combination of tuples ------------------------------------------------------- #
def combine_state(fsm, conflict_var_lst, program_sequence, state_map, loop_flag):

    for state_idx in range(len(fsm.states) - 1, 0, -1):
        state_now = state_map["Q" + str(state_idx)]
        state_previous = state_map["Q" + str(state_idx - 1)]

        if set(state_now.Equality) == set(state_previous.Equality) and \
           set(state_now.Disequality) == set(state_previous.Disequality) and \
           state_now.Function == state_previous.Function:  #  whether the two state is the same


            # the same tuples don't mean combination, we still need to consider the related statement.
            # for example:
            # current equality is x=y, and we executed x:=f(x)*3; y:=f(y)*3
            # althouth the tuple after the second and the third x:=f(x) is the same, we can't do combination
            statement = program_sequence[state_idx - 1] # consider the statement before entering the state

            if ":=" in statement and not ("(" in statement):            # x := y
                left_var = statement[:statement.find(":") - 1]
                if left_var in conflict_var_lst[state_idx - 1]:  # related statement, can't do combination
                    pass
                else:
                    fsm.combine_state(state_idx - 1, state_idx, state_map, program_sequence, loop_flag)
                    # update conflict_var_lst
                    conflict_var_lst = conflict_var_lst[0: state_idx] + conflict_var_lst[state_idx + 1:]

            elif ":=" in statement and ("(" in statement):              # x := f(y)
                left_var = statement[:statement.find(":") - 1]
                if left_var in conflict_var_lst[state_idx - 1]:  # related statement, can't do combination
                    pass
                else:
                    fsm.combine_state(state_idx - 1, state_idx, state_map, program_sequence, loop_flag)
                    # update conflict_var_lst
                    conflict_var_lst = conflict_var_lst[0: state_idx] + conflict_var_lst[state_idx + 1:]

            elif "==" in statement:                                     # assume(x == y)
                left_var = statement[statement.find("(") + 1: statement.rfind("=") - 2]
                right_var = statement[statement.rfind("=") + 2: statement.find(")")]
                abandon_flag = True
                for conflict_var in conflict_var_lst[:state_idx]:   # to check if the previous conflict variable is related, if yes then must preserve
                    if left_var in conflict_var or right_var in conflict_var:
                        abandon_flag = False
                        break
                if abandon_flag:                                        # the previous conflict variable isn't related to the assume statement
                    fsm.combine_state(state_idx - 1, state_idx, state_map, program_sequence, loop_flag)
                    # update conflict_var_lst
                    conflict_var_lst = conflict_var_lst[0: state_idx] + conflict_var_lst[state_idx + 1:]

            elif "!=" in statement:  # assume(x != y)
                fsm.combine_state(state_idx - 1, state_idx, state_map, program_sequence, loop_flag)
                # update conflict_var_lst
                conflict_var_lst = conflict_var_lst[0: state_idx] + conflict_var_lst[state_idx + 1:]



def loop_verification(entry_point_1, entry_point_2, exit_point, state_map, program_sequence):
    i = 1
    always_flag = False
    while entry_point_1 + i < entry_point_2 and entry_point_2 + i < exit_point: #  check the length of loop-body
        new_1 = entry_point_1 + i
        new_2 = entry_point_2 + i
        state_1 = state_map["Q" + str(new_1)]
        state_2 = state_map["Q" + str(new_2)]
        # check the same states, and then, check the same statements expect for ghost variable statement
        if set(state_1.Equality) == set(state_2.Equality) and \
           set(state_1.Disequality) == set(state_2.Disequality) and \
           program_sequence[new_1 - 1] == program_sequence[new_2 - 1]:
           # state_1.Function == state_2.Function and \
            if i == entry_point_2 - entry_point_1 - 1:      # the last one matched
                always_flag = True
            i += 1
        else:
            always_flag = False
            break
    return always_flag

def loop_detection(initial_point, exit_point, loop_points, state_map, program_sequence):
    initial_index = loop_points.index(initial_point)
    for i in range(initial_index, len(loop_points)):
        entry_point_1 = loop_points[i]
        state_1 = state_map["Q" + str(entry_point_1)]
        for j in range(i + 1, len(loop_points)):
            entry_point_2 = loop_points[j]
            state_2 = state_map["Q" + str(entry_point_2)]

            # check the same states and statements
            if program_sequence[entry_point_1-1] == program_sequence[entry_point_2-1] and \
               set(state_1.Equality) == set(state_2.Equality) and \
               set(state_1.Disequality) == set(state_2.Disequality):
               # set(state_1.Disequality) == set(state_2.Disequality) and \
               # state_1.Function == state_2.Function:

                if loop_verification(entry_point_1, entry_point_2, exit_point, state_map, program_sequence):  # find all possible matched results
                    return entry_point_1, entry_point_2

    return None, None

def combine_loop(fsm, dir, program_sequence, state_map, loop_flag):

    loops = []  # store the loop-entry tuple [xx, xx] to be combined
    guards = [] # store the corresponded guard statement


    # find the potential combination and store into loops/guards
    initial_point_index = 0
    loop_points = [i for i, x in enumerate(loop_flag) if x == 1]
    if -1 in loop_flag:
        # exit_point = loop_flag.index(-1)
        exit_point = len(loop_flag) - loop_flag[::-1].index(-1) - 1
        while initial_point_index < len(loop_points) - 1: # reach the last entry then exit
            initial_point = loop_points[initial_point_index]
            [ret1, ret2] = loop_detection(initial_point, exit_point, loop_points, state_map, program_sequence)
            if ret1 != None:
                loops.append([ret1, ret2])
                guards.append([dir[program_sequence[ret1-1]], dir[program_sequence[ret2+(ret2-ret1)-1]]])
                initial_point_index = loop_points.index(ret2) + 1
            else:   # there is no potential combination
                break

    # do combination for loop
    if len(loops) != 0:
        fsm.combine_loop(loops, guards, state_map, program_sequence)




# -----------------------------------------------other auxiliaty func------------------------------------------------------------- #
# print state_map
def print_state_map(state_map):
    print("========================")
    print(state_map)
    for i in range(len(state_map.keys())):
        Q = state_map["Q" + str(i)]
        print("Q" + str(i))
        print(Q.Equality)
        print(Q.Disequality)
        print(Q.Function)
        print("========================")


# ---------------------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":

    pass