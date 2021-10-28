#!/usr/bin/env python
#-*- coding:utf-8 -*-
import copy
from Verifier4UP.src.Parser.color import cyan_none
from Verifier4UP.src.Parser.parsing_bpl import parsing_bpl
from Verifier4UP.src.Parser.parsing_trace import parsing_trace
from Verifier4UP.src.Parser.assert_2_assume import assert_2_assume
from Verifier4UP.src.TripleGeneration.collection_triple import collection_info
from Verifier4UP.src.Coherence.Trace_Coherence.translator import translator
from Verifier4UP.src.Coherence.Trace_Coherence.check_trace_coherent import check_trace_coherent
from Verifier4UP.src.AutomataGeneralization.automata_info import automata
from Verifier4UP.src.AutomataGeneralization.auxiliary import simplify_triple, combine_loop, combine_state, eliminate_ghost, find_never_used_vars

#
# given a string corresponded to .tr
# first translating into coherent trace
# then begin verification:
# if feasible (state="accept"), then find the counterexample and return False
# else generating the corresponded generalized automata and return True
#

def generalized_automata(trace, bpl, save_file=False, plot_flag=False, print_flag=False, detail_flag=False):



    # ------------------------------------------------------------------------------------------- #
    # ----------------------------------------- trace parser ------------------------------------ #
    # ------------------------------------------------------------------------------------------- #

    # -------------------1.ensure the trace satisfy coherence------------------- #
    coherence = check_trace_coherent(trace, print_flag=False, detail_flag=False)
    if coherence:
        if print_flag:
            print("++ Check Coherence: ")
            print("Congratulation! You got a coherent trace.")
            print("-------------------------------------------------------\n")
    else:
        trace = translator(trace, save_file=False, print_flag=False)
        if print_flag:
            print("++ Check Coherence: ")
            print("Oh Bad!! coherence is unsatisfied.")
            print("-------------------------------------------------------\n")
    if save_file:
        with open("./counter_example_trace.tr", 'w') as f:
            f.write(trace)

    trace_lst = trace.split("\n")
    for i in range(len(trace_lst) - 1, -1, -1):
        if trace_lst[i] == "":
            del trace_lst[i]

    # -------------------2.get the info of trace and loop------------------- #
    [vars, funs, program_sequence, loop_flag] = parsing_trace(trace, print_flag=False)
    if print_flag:
        print("++ Parsing Trace: ")
        print("trace sequence: \n", program_sequence)
        print("benchmark flag: \n", loop_flag)
        print("-------------------------------------------------------\n")

    # -------------------------- 3.get dir --------------------------------- #
    dir = parsing_bpl(bpl)
    origin_dir = copy.deepcopy(dir)     # preserve the original dir for eliminating automata in the last
    current_max_alphabet = max(dir.values())
    if current_max_alphabet == "Z":
        alphabet_idx = ord('a')
    else:
        alphabet_idx = ord(current_max_alphabet) + 1
    # if current_max_alphabet[1] == "z":
    #     alphabet_idx_1 = ord(current_max_alphabet[0]) + 1
    #     alphabet_idx_2 = ord("a")
    # else:
    #     alphabet_idx_1 = ord(current_max_alphabet[0])
    #     alphabet_idx_2 = ord(current_max_alphabet[1]) + 1
    for line in trace_lst:
        line = line.strip()
        statement = line[:line.find(";")]
        if not (statement in dir.keys()):
            dir[statement] = chr(alphabet_idx)
            if chr(alphabet_idx) == "Z":
                alphabet_idx = ord('a')
            else:
                alphabet_idx += 1
            # dir[statement] = chr(alphabet_idx_1) + chr(alphabet_idx_2)
            # if chr(alphabet_idx_2) == "z":
            #     alphabet_idx_1 += 1
            #     alphabet_idx_2 = ord('a')
            # else:
            #     alphabet_idx_2 += 1
    if print_flag:
        print_dir = sorted(dir.items(), key=lambda x: x[1], reverse=False)
        print("dir: ")
        for item in print_dir:
            print(item[1], ":", item[0])
        print("\n\n-------------------------------------------------------")
    reverse_dir = {}
    for key in dir.keys():
        reverse_dir[dir[key]] = key



    # --------------4.get the tuple info of trace, check feasiblility--------------- #
    state_map = collection_info(trace)
    if state_map["Q" + str(len(state_map.keys())-1)].state == "accept":                 # find a feasible error trace
        current_trace = ""
        for stat in program_sequence:
            current_trace = current_trace + stat + "; "
        print(cyan_none % "feasible error trace: " + current_trace)
        return False, ""

    # --------------------------5.get the irrelevant variable------------------------------ #
    never_used_vars = find_never_used_vars(program_sequence)
    used_vars = []
    for var in vars:
        if not (var in never_used_vars):
            used_vars.append(var)
    conflict_var_lst = [used_vars]*(len(program_sequence)) + ["NULL"]
    if detail_flag:
        print("++ never used var: \n", never_used_vars)
        print("-------------------------------------------------------\n")

    # ---------------------6.simplify tuples based on the irrelevant variable---------------------- #
    if detail_flag:
        print("++ simplified triple: ")
    for i in range(len(conflict_var_lst)):
        triple = state_map["Q" + str(i)]
        conflict_var = conflict_var_lst[i]
        simplify_triple(triple, conflict_var)   # tackle with state_map["Q" + str(i)]
        if detail_flag:
            print("========================")
            print("Q" + str(i))
            print(triple.Equality)
            print(triple.Disequality)
            print(triple.Function)
            if i <= len(program_sequence)-1: print(program_sequence[i])
    if detail_flag:
        print("-------------------------------------------------------\n")










    # ------------------------------------------------------------------------------------------- #
    # ----------------------------------------- get automata ------------------------------------ #
    # ------------------------------------------------------------------------------------------- #

    # ----------------------------1.initial automat------------------------ #
    fsm = automata(alphabet=sorted(list(dir.values())), states=[0], initial_state=0, accepted_states=[len(program_sequence)], transition=[])
    state_idx = 0
    for statement in program_sequence:
        fsm.add_transition([state_idx, dir[statement], state_idx+1])
        state_idx += 1
    for i in range(len(state_map.keys())):  # add self-loop for rejected state
        if state_map["Q"+str(i)].state == "reject":
            for action in dir.keys():
                fsm.add_transition([len(fsm.states)-1, dir[action], len(fsm.states)-1])
    if print_flag:
        fsm.show("M_initial", flag=True)
        print("-------------------------------------------------------")

    # ------------------------2.for ghost variables------------------------- #
    eliminate_ghost(origin_dir, state_map, fsm, dir, program_sequence, loop_flag)
    # fsm.visualization(reverse_dir)
    if print_flag:
        fsm.show("M_eliminate_ghost", flag=True)
        print("-------------------------------------------------------")

    # ----------------------3.loop-combination based on the simplified tuples ------------------- #
    combine_loop(fsm, dir, program_sequence, state_map, loop_flag)
    # fsm.visualization(reverse_dir)
    if print_flag:
        fsm.show("M_loop_refinement", flag=True)
        print("-------------------------------------------------------")

    # ----------------------4.state-combination based on the simplified tuples并------------------- #
    # combine_state(fsm, conflict_var_lst, program_sequence, state_map, loop_flag)
    # fsm.visualization(reverse_dir)
    # if print_flag:
    #     fsm.show("M_state_refinement", flag=True)
    #     print("-------------------------------------------------------")


    # ------------------------5.write into file------------------------- #
    log_final = fsm.show("M_trace")
    if plot_flag == True:
        fsm.visualization(reverse_dir)
    if save_file:
        with open("./trace_automata.ats", "w") as file:
            file.write(log_final)

    return True, log_final




if __name__ == "__main__":


    # trace_file = "../benchmark/Trace/combine_state.tr"
    # trace_file = "../benchmark/Trace/combine_loop1.tr"
    # trace_file = "../benchmark/Trace/combine_loop2.tr"
    # trace_file = "../benchmark/Trace/non_memorizing.tr"
    # trace_file = "../benchmark/Trace/non_earlyassume.tr"

    # ------------------------- test example -------------------------------------#
    trace_file = "../benchmark/Trace/test.tr"

    boogie_file = trace_file.replace("Trace", "Program").replace(".tr", "_ori.bpl")
    trace = ""
    with open(trace_file, 'r') as f:
        for line in f:
            trace = trace + line
    bpl = assert_2_assume(boogie_file)
    [bool_result, ats] = generalized_automata(trace, bpl, save_file=True, plot_flag=True, print_flag=True, detail_flag=True)
