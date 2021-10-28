#!/usr/bin/env python
#-*- coding:utf-8 -*-
import copy
from Verifier4UP.src.Coherence.quad_info import quad_info
from Verifier4UP.src.Parser.parsing_trace import parsing_trace
from Verifier4UP.src.TripleGeneration.transition_rule import rule1, rule2, rule3, rule4


#
# give a string corresponded to .tr, check whether is's coherent trace
# yes then True, no then False
#



def check_trace_coherent(trace, print_flag=False, detail_flag=False):

    # ------------------------------------------------------------------------------------------- #
    # ----------------------------------------- get info ---------------------------------------- #
    # ------------------------------------------------------------------------------------------- #

    [vars, funs, program_sequence, loop_flag] = parsing_trace(trace, print_flag=False)
    if print_flag:
        print("++ Parsing Trace: ")
        print("trace sequence: \n", program_sequence)
        print("-------------------------------------------------------\n")
        print("++ Check Coherence: ")




    # ------------------------------------------------------------------------------------------- #
    # ---------------------------------- check based on tuple ----------------------------------- #
    # ------------------------------------------------------------------------------------------- #
    state_map = {}
    # initial state
    state_map["Q0"] = quad_info(vars, funs, 0)
    if detail_flag:
        state_map["Q0"].show()


    current_index = 0
    for stat in program_sequence:


        # check whether there exists a threat for coherence
        if (":=" in stat and "(" in stat) or "==" in stat:  # assume(x == y)  or x := f(y)
            Q = state_map["Q"+str(current_index)]
            [coherent_flag, statement_type] = Q.check_coherent(stat)
            if coherent_flag == False:
                if print_flag:
                    print("Oh Bad!! coherence is unsatisfied, as " + stat + " violates " + statement_type + ".")
                return False


        next_index = current_index + 1
        # copy the current quad
        Q_next = quad_info(vars, funs, next_index)
        Q_next.equivalence = copy.deepcopy(state_map["Q" + str(current_index)].equivalence)
        Q_next.Equality = copy.deepcopy(state_map["Q" + str(current_index)].Equality)
        Q_next.Disequality = copy.deepcopy(state_map["Q" + str(current_index)].Disequality)
        Q_next.Function = copy.deepcopy(state_map["Q" + str(current_index)].Function)
        Q_next.Item = copy.deepcopy(state_map["Q" + str(current_index)].Item)

        # update the quad
        if ":=" in stat and not("(" in stat):   # x := y
            Q_next = rule1(stat, Q_next)
        elif ":=" in stat and ("(" in stat):    # x := f(y)
            Q_next = rule2(stat, Q_next)
        elif "==" in stat:                      # assume(x == y)
            Q_next = rule3(stat, Q_next)
        elif "!=" in stat:                      # assume(x != y)
            Q_next = rule4(stat, Q_next)
        Q_next.update(stat)
        state_map["Q" + str(next_index)] = Q_next

        current_index = next_index

        # print result
        if detail_flag:
            print("++++ after ", stat)
            state_map["Q" + str(next_index)].show()

    if print_flag:
        print("Congratulation! You got a coherent trace.")

    return True


if __name__ == "__main__":

    trace_file = "../../benchmark/Trace/memorizing.tr"
    # trace_file = "../../benchmark/Trace/non_memorizing.tr"
    # trace_file = "../../benchmark/Trace/earlyassume.tr"
    # trace_file = "../../benchmark/Trace/non_earlyassume.tr"

    # ------------------------- test example -------------------------------------#
    # trace_file = "../../Coherence/Program_Coherence/check_trace_property.tr"



    trace = ""
    with open(trace_file, "r") as f:
        for line in f:
            trace = trace + line
    check_trace_coherent(trace, print_flag=True, detail_flag=True)
