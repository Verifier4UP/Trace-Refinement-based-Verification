#!/usr/bin/env python
#-*- coding:utf-8 -*-
import copy
from Verifier4UP.src.Parser.parsing_trace import parsing_trace
from Verifier4UP.src.Coherence.quad_info import quad_info
from Verifier4UP.src.Coherence.auxiliary import item_info_loss
from Verifier4UP.src.Coherence.Trace_Coherence.check_trace_coherent import check_trace_coherent
from Verifier4UP.src.TripleGeneration.transition_rule import rule1, rule2, rule3, rule4


#
# give a string corresponded to .tr, do translator
# if it's coherent, then do nothing
# else translate non-coherence into coherence
# return a string w.r.t. trace
# If need to save, generate trace_origin.tr and trace_coherent.tr
#


def translator(trace, save_file=False, print_flag=False):

    if save_file:
        with open("./trace_origin.tr", 'w') as f:
            f.write(trace)


    coherence = check_trace_coherent(trace, print_flag=False, detail_flag=False)
    if coherence:
        if print_flag:
            print("Congratulation! You got a coherent trace.")
    else:
        # add ghost variable
        ghost_var_idx = 0
        while coherence == False:
            [vars, funs, program_sequence, loop_flag] = parsing_trace(trace, print_flag=False)
            new_program_sequence = translator_once(trace, ghost_var_idx)
            if print_flag:
                print("Oh Bad!! coherence is unsatisfied.")
                print("after " + str(ghost_var_idx) + " update, new trace sequence: \n", new_program_sequence)
            coherent_trace = ""
            for i in range(len(new_program_sequence)):
                # Be sure to keep the loop point information when writing
                if new_program_sequence[i] == program_sequence[i]:  # the same statement
                    statement = new_program_sequence[i]
                    if loop_flag[i+1] == 1:       # loop-entry
                        coherent_trace = coherent_trace + statement + "; -Entry\n"
                    elif loop_flag[i+1] == -1:    # loop-exit
                        coherent_trace = coherent_trace + statement + "; -Exit\n"
                    else:
                        coherent_trace = coherent_trace + statement + ";\n"
                else:
                    statement = new_program_sequence[i]
                    coherent_trace = coherent_trace + statement + ";\n"
                    for j in range(i, len(program_sequence)):
                        statement = program_sequence[j]
                        if loop_flag[j+1] == 1:       # loop-entry
                            coherent_trace = coherent_trace + statement + "; -Entry\n"
                        elif loop_flag[j+1] == -1:    # loop-exit
                            coherent_trace = coherent_trace + statement + "; -Exit\n"
                        else:
                            coherent_trace = coherent_trace + statement + ";\n"
                    break
            trace = coherent_trace
            coherence = check_trace_coherent(trace, print_flag=False, detail_flag=False)
            ghost_var_idx += 1

        if print_flag:
            print("Congratulation! Now, You got a coherent trace.")

    if save_file:
        with open("./trace_coherent.tr", 'w') as f:
            f.write(trace)

    return trace



def translator_once(trace, ghost_var_idx):

    [vars, funs, program_sequence, loop_flag] = parsing_trace(trace, print_flag=False)


    state_map = {}
    # initial state
    state_map["Q0"] = quad_info(vars, funs, 0)

    current_index = 0
    for stat in program_sequence:


        # -------------------------------- update state ----------------------------------- #
        next_index = current_index + 1
        # copy the current quad
        Q_next = quad_info(vars, funs, next_index)
        Q_next.equivalence = copy.deepcopy(state_map["Q" + str(current_index)].equivalence)
        Q_next.Equality = copy.deepcopy(state_map["Q" + str(current_index)].Equality)
        Q_next.Disequality = copy.deepcopy(state_map["Q" + str(current_index)].Disequality)
        Q_next.Function = copy.deepcopy(state_map["Q" + str(current_index)].Function)
        Q_next.Item = copy.deepcopy(state_map["Q" + str(current_index)].Item)

        # update the quad
        if ":=" in stat and not ("(" in stat):  # x := y
            Q_next = rule1(stat, Q_next)
        elif ":=" in stat and ("(" in stat):  # x := f(y)
            Q_next = rule2(stat, Q_next)
        elif "==" in stat:  # assume(x == y)
            Q_next = rule3(stat, Q_next)
        elif "!=" in stat:  # assume(x != y)
            Q_next = rule4(stat, Q_next)
        Q_next.update(stat)



        # ---------------------------------check whether there is missing information in the new state----------------------------- #
        if ":=" in stat: # only x := f(y) and x := y related to term-rewriting， which might cause non-coherence(especially, memorizing)
            [flag, item] = item_info_loss(Q_next, state_map["Q" + str(current_index)], stat)
        else:
            flag = False

        # location for debugger
        # if stat == "x := next(x)":
        #     state_map["Q" + str(current_index)].show()
        #     Q_next.show()
        #     print(flag)
        #     print("=======")

        if flag:  # lose information
            new_stat = "g" + str(ghost_var_idx) + " := " + item
            new_program_sequence = program_sequence[:current_index] + [new_stat] + program_sequence[current_index:]
            return new_program_sequence

        else:
            # store and check the next statement
            state_map["Q" + str(next_index)] = Q_next
            current_index = next_index






if __name__ == "__main__":



    trace_file = "../../benchmark/Trace/memorizing.tr"
    # trace_file = "../../benchmark/Trace/non_memorizing.tr"
    # trace_file = "../../benchmark/Trace/earlyassume.tr"
    # trace_file = "../../benchmark/Trace/non_earlyassume.tr"

    # ------------------------- test example -------------------------------------#


    trace = ""
    with open(trace_file, 'r') as f:
        for line in f:
            trace = trace + line
    new_trace = translator(trace, save_file=True, print_flag=True)

