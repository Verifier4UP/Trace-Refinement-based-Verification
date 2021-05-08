#!/usr/bin/env python
#-*- coding:utf-8 -*-
import copy
from Verifier4UP.src.Parser.parsing_trace import parsing_trace
from Verifier4UP.src.TripleGeneration.triple_info import triple
from Verifier4UP.src.TripleGeneration.transition_rule import rule1, rule2, rule3, rule4

#
# Give a trace (.tr) to collect the triple information corresponding to each step of the trace
# storage into state_map, and return
#



def collection_info(trace, print_flag = False):


    # ------------------------------- parser file --------------------------------------- #
    [vars, funs, program_sequence, loop_flag] = parsing_trace(trace, print_flag=False)
    if print_flag:
        print("++ Parsing Trace: ")
        print("trace sequence: \n", program_sequence)
        print("benchmark flag: \n", loop_flag)
        print("-------------------------------------------------------\n")
        print("++ Collecting Triple Info: ")




    # ------------------------------- get triple -------------------------------------- #

    state_map = {}
    # initial state
    state_map["Q0"] = triple(vars, funs, 0)
    if print_flag==True:
        state_map["Q0"].show()

    current_index = 0
    for stat in program_sequence:
        # trace debugging by break point
        # state_map["Q"+str(current_index)].show()
        # print(stat)

        next_index = current_index + 1
        # if there exist a reject state, then the state after this state should be rejected
        if state_map["Q" + str(current_index)].state == "reject":
            Qr = triple(vars, funs, next_index)
            Qr.Equality = state_map["Q" + str(current_index)].Equality
            Qr.Disequality = state_map["Q" + str(current_index)].Disequality
            Qr.Function = state_map["Q" + str(current_index)].Function
            Qr.equivalence = state_map["Q" + str(current_index)].equivalence
            Qr.state = "reject"
            state_map["Q" + str(next_index)] = Qr

        else:
            # copy the current triple
            Q_next = triple(vars, funs, next_index)
            Q_next.equivalence = copy.deepcopy(state_map["Q" + str(current_index)].equivalence)
            Q_next.Equality = copy.deepcopy(state_map["Q" + str(current_index)].Equality)
            Q_next.Disequality = copy.deepcopy(state_map["Q" + str(current_index)].Disequality)
            Q_next.Function = copy.deepcopy(state_map["Q" + str(current_index)].Function)

            # update the triple
            if ":=" in stat and not("(" in stat):   # x := y
                Q_next = rule1(stat, Q_next)
            elif ":=" in stat and ("(" in stat):    # x := f(y)
                Q_next = rule2(stat, Q_next)
            elif "==" in stat:                      # assume(x == y)
                Q_next = rule3(stat, Q_next)
            elif "!=" in stat:                      # assume(x != y)
                Q_next = rule4(stat, Q_next)
            Q_next.update()
            state_map["Q" + str(next_index)] = Q_next

        current_index = next_index


        if print_flag == True:
            print("++++ after ", stat)
            state_map["Q" + str(next_index)].show()

    return state_map


if __name__ == "__main__":

    trace_file = "../benchmark/Trace/memorizing.tr"
    # trace_file = "../benchmark/Trace/non_memorizing.tr"
    # trace_file = "../benchmark/Trace/earlyassume.tr"
    # trace_file = "../benchmark/Trace/non_earlyassume.tr"


    # ------------------------- test example -------------------------------------#
    # trace_file = "../benchmark/Trace/test.tr"



    trace = ""
    with open(trace_file, "r") as f:
        for line in f:
            trace = trace + line
    collection_info(trace, print_flag=True)
