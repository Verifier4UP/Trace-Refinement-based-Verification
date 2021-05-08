#!/usr/bin/env python
#-*- coding:utf-8 -*-
import copy
import time
import random
import numpy as np
from Verifier4UP.src.Parser.color import cyan_none
from Verifier4UP.src.Parser.parsing_bpl import parsing_bpl
from Verifier4UP.src.Coherence.auxiliary import get_while_guard
from Verifier4UP.src.CEGAR.auxiliary_ultimate import translate_albet_to_stat_print
from Verifier4UP.src.Coherence.quad_info import quad_info
from Verifier4UP.src.Coherence.auxiliary import get_fun_var
from Verifier4UP.src.TripleGeneration.triple_info import triple
from Verifier4UP.src.TripleGeneration.transition_rule import rule1, rule2, rule3, rule4
from Verifier4UP.src.TripleGeneration.collection_triple import collection_info


#
# given the strings corresponded to .ats and .bpl
# given the property to be verified (triple, check-feasible), (quad-info, check-coherence)
# Use fix point alg to verify the traces one by one
# if all paths meet the properties, return True; otherwise, return False
#


def fix_point_alg(ats, bpl, info_class, func, save_file=False, print_flag=False):

    ats_lst = ats.split("\n")
    bpl_lst = bpl.split("\n")
    check_time = 0


    # ----------------------------- get info from bpl ---------------------------- #
    # dir
    dir = parsing_bpl(bpl, print_flag=False)
    reverse_dir = {}
    for key in dir.keys():
        reverse_dir[dir[key]] = key
    # guard statement
    [entry_point, exit_point] = get_while_guard(bpl)
    # func's variable info
    [vars, funs] = get_fun_var(bpl)

    # if print_flag:
    #     print_dir = sorted(dir.items(), key=lambda x: x[1], reverse=False)
    #     for item in print_dir:
    #         print(item[1], ":", item[0])
    #     print("\n")


    # -------------------------------------- get each state's transition from ats ---------------------------- #
    # for example: degree_dir = {"q0": [["A", "q1"]], "q1"： [["B", "q2"], ["C", "q3"]], ....}
    flag = False
    degree_dir = {}
    for line in ats_lst:
        if flag:
            if "}" in line:
                break
            line = line.strip()[1:-1].split(" ")
            if line[0] in degree_dir.keys():
                degree_dir[line[0]].append([line[1], line[2]])
            else:
                degree_dir[line[0]] = [[line[1], line[2]]]
        if "transition" in line:
            flag = True

    # if print_flag:
    #     for item_key in degree_dir.keys():
    #         print(item_key, ": ", degree_dir[item_key])
    #     print("\n\n")


    # ----------------------------------------- Find a trace contained repeated loop  ------------------------------------------ #
    work_list = [""]                                        # each block_trace's statement
    work_list_last_choice = {"": "q0"}                      # each block_trace's last state
    work_list_last_info = {"": info_class(vars, funs, 0)}   # each block_trace's last n-tuple info
    work_list_loop_info = {"": []}                          # each block_trace's n-tuple info w.r.t. loop
    work_list_loop_num = {"": 0}                            # the loop's iteration num
    check_flag = 0
    while len(work_list) != 0:
        ## BFS
        select_one = ""
        least_num = np.inf
        for key_trace in work_list_loop_num.keys():         #  prefer to the one with less iteration num
            if work_list_loop_num[key_trace] < least_num:
                least_num = work_list_loop_num[key_trace]
                select_one = key_trace

        current_trace = select_one
        current_choice = work_list_last_choice[current_trace]
        current_info = work_list_last_info[current_trace]
        current_loop_info = work_list_loop_info[current_trace]
        current_loop_num = work_list_loop_num[current_trace]
        work_list.remove(current_trace)
        del work_list_last_choice[current_trace]
        del work_list_last_info[current_trace]
        del work_list_loop_info[current_trace]
        del work_list_loop_num[current_trace]

        # check_begin = time.time()
        # each_check_begin = time.time()
        # -------------------------------- check property--------------------------------- #
        if current_trace != "":
            # delete the property violated trace, whenever whether it has been extended to the exit of the program

            # Check randomly, or check when reach the exit
            if check_flag % 10 == 0 or not(current_choice in degree_dir.keys()):

                # write trace into .tr
                check_trace_property = ""
                trace = current_trace.split(" ")[:-1]
                for action in trace:
                    statement = reverse_dir[action]
                    if statement in entry_point:
                        check_trace_property = check_trace_property + statement + "; -Entry\n"
                    elif statement in exit_point:
                        check_trace_property = check_trace_property + statement + "; -Exit\n"
                    else:
                        check_trace_property = check_trace_property + statement + ";\n"
                if save_file:
                    with open("./check_trace_property.tr", 'w') as f:
                        f.write(check_trace_property)
                        
                #  check the coherence
                if info_class == quad_info:
                    # for coherence
                    # Regardless of whether the trace reaches the exit or not,
                    # as long as it is found to violate the property, then the entire program is violated
                    if func(check_trace_property) == False:           #  non-coherent trace
                        if print_flag:
                            print(translate_albet_to_stat_print(dir, current_trace[:-1]))
                            print("violates coherence\n")
                        return False
                    else:
                        if not(current_choice in degree_dir.keys()):  # If the trace satisfies the property has reached the end, then continue
                            continue


                # check correctness
                if info_class == triple:
                    # Only when the trace reaches the exit and is feasible, it is said that it violates the property
                    # and the infeasible traces can be discarded in advance
                    if func(check_trace_property) == False and not(current_choice in degree_dir.keys()):  # feasible trace
                        print(cyan_none % "feasible error trace: " + translate_albet_to_stat_print(dir, current_trace[:-1]))
                        return False
                    if func(check_trace_property) == True:
                        if print_flag:
                            print(translate_albet_to_stat_print(dir, current_trace[:-1]))
                            print("is infeasible.\n")
                        continue


            # check_end = time.time()
            # check_time = check_time + (check_end-check_begin)
            # print("check time: ", str(check_time))
        check_flag += 1





        # each_check_end = time.time()
        # each_extension_begin = time.time()
        # ---------------------- extension --------------------------------- #
        # Take out the last state for the next transition
        if len(degree_dir[current_choice]) == 1:                   # sequential
            action = degree_dir[current_choice][0][0]
            next_choice = degree_dir[current_choice][0][1]

            # Update based on the existing n-tuple state and statement
            stat = reverse_dir[action]
            next_info = current_info
            # update the info
            if ":=" in stat and not ("(" in stat):  # x := y
                next_info = rule1(stat, next_info)
            elif ":=" in stat and ("(" in stat):  # x := f(y)
                next_info = rule2(stat, next_info)
            elif "==" in stat:  # assume(x == y)
                next_info = rule3(stat, next_info)
            elif "!=" in stat:  # assume(x != y)
                next_info = rule4(stat, next_info)
            if info_class == triple:
                next_info.update()
            else:
                next_info.update(stat)

            new_trace = current_trace + action + " " # initial is ""，need an action
            # update work_list
            work_list.append(new_trace)
            work_list_last_choice[new_trace] = next_choice
            work_list_last_info[new_trace] = next_info
            work_list_loop_info[new_trace] = current_loop_info
            work_list_loop_num[new_trace] = current_loop_num



        elif len(degree_dir[current_choice]) == 2:                           # if_else / while

            action1 = degree_dir[current_choice][0][0]
            action2 = degree_dir[current_choice][1][0]
            next_choice1 = degree_dir[current_choice][0][1]
            next_choice2 = degree_dir[current_choice][1][1]
            stat1 = reverse_dir[action1]
            stat2 = reverse_dir[action2]


            # new loop, before making a choice, first see if the current state has appeared
            discard = ""
            if stat1 in entry_point:
                for Q in current_loop_info:     # Determine whether there are equal n-tuple states
                    if info_class == quad_info and \
                            Q.Equality == current_info.Equality and \
                            Q.Disequality == current_info.Disequality and \
                            Q.Function == current_info.Function and \
                            Q.Item == current_info.Item:
                        discard = "stat1"
                    elif info_class == triple and \
                            Q.Equality == current_info.Equality and \
                            Q.Disequality == current_info.Disequality and \
                            Q.Function == current_info.Function:
                        discard = "stat1"
            elif stat2 in entry_point:
                for Q in current_loop_info:  # Determine whether there are equal n-tuple states
                    if info_class == quad_info and \
                            Q.Equality == current_info.Equality and \
                            Q.Disequality == current_info.Disequality and \
                            Q.Function == current_info.Function and \
                            Q.Item == current_info.Item:
                        discard = "stat2"
                    elif info_class == triple and \
                            Q.Equality == current_info.Equality and \
                            Q.Disequality == current_info.Disequality and \
                            Q.Function == current_info.Function:
                        discard = "stat2"


            if discard != "stat1":
                # Update based on the existing n-tuple state and statement
                next_info1 = copy.deepcopy(current_info)
                # update the info
                if ":=" in stat1 and not ("(" in stat1):  # x := y
                    next_info1 = rule1(stat1, next_info1)
                elif ":=" in stat1 and ("(" in stat1):  # x := f(y)
                    next_info1 = rule2(stat1, next_info1)
                elif "==" in stat1:  # assume(x == y)
                    next_info1 = rule3(stat1, next_info1)
                elif "!=" in stat1:  # assume(x != y)
                    next_info1 = rule4(stat1, next_info1)
                if info_class == triple:
                    next_info.update()
                else:
                    next_info.update(stat1)

                new_trace1 = current_trace + action1 + " "  # initial is ""，need an action
                # update work_list
                work_list.append(new_trace1)
                work_list_last_choice[new_trace1] = next_choice1
                work_list_last_info[new_trace1] = next_info1
                if stat1 in entry_point:     # current_info is a loop-entry
                    work_list_loop_info[new_trace1] = copy.deepcopy(current_loop_info) + [current_info]
                    work_list_loop_num[new_trace1] = current_loop_num + 1
                else:
                    work_list_loop_info[new_trace1] = copy.deepcopy(current_loop_info)
                    work_list_loop_num[new_trace1] = current_loop_num



            # ----------------------------------------------------------------------------- #

            if discard != "stat2":
                # Update based on the existing n-tuple state and statement
                next_info2 = copy.deepcopy(current_info)
                # update the info
                if ":=" in stat2 and not ("(" in stat2):  # x := y
                    next_info2 = rule1(stat2, next_info2)
                elif ":=" in stat2 and ("(" in stat2):  # x := f(y)
                    next_info2 = rule2(stat2, next_info2)
                elif "==" in stat2:  # assume(x == y)
                    next_info2 = rule3(stat2, next_info2)
                elif "!=" in stat2:  # assume(x != y)
                    next_info2 = rule4(stat2, next_info2)
                if info_class == triple:
                    next_info.update()
                else:
                    next_info.update(stat2)

                new_trace2 = current_trace + action2 + " "  # initial is ""，need an action
                # update work_list
                work_list.append(new_trace2)
                work_list_last_choice[new_trace2] = next_choice2
                work_list_last_info[new_trace2] = next_info2
                if stat2 in entry_point:  # current_info is a loop-entry
                    work_list_loop_info[new_trace2] = copy.deepcopy(current_loop_info) + [current_info]
                    work_list_loop_num[new_trace2] = current_loop_num + 1
                else:
                    work_list_loop_info[new_trace2] = copy.deepcopy(current_loop_info)
                    work_list_loop_num[new_trace2] = current_loop_num

        # each_extension_end = time.time()
        # print("ratio: ", (each_check_end-each_check_begin)/(each_extension_end-each_extension_begin))

    return True



if __name__ == "__main__":
    pass