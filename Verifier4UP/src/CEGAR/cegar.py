#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import time
from Verifier4UP.src.CEGAR.DFA import inverse, intersection
from Verifier4UP.src.Parser.assert_2_assume import assert_2_assume
from Verifier4UP.src.ProgramToAutomata.cfg_automata import boogie_to_automata
from Verifier4UP.src.Parser.color import red_none
from Verifier4UP.src.Parser.parsing_bpl import parsing_bpl
from Verifier4UP.src.AutomataGeneralization.generalization import generalized_automata
from Verifier4UP.src.Coherence.auxiliary import get_while_guard
from Verifier4UP.src.CEGAR.auxiliary import check_empty, trans_fsm, translate_albet_to_stat_save, translate_albet_to_stat_print

#
# give a string corresponded to .ats, do trace refinement
# If it finds a feasible (state="accept") within the specified time, the verification result is "False" and the timeout result is "False";
# If the verification is successful within the specified time, the verification result is "True" and the timeout result is "False";
# If it is not terminated within the specified time, the verification result is "False" and the timeout result "True" is returned
# If an error occurs, the verification result is "NULL" and the timeout result is "False"
#


def trace_refinement(ats, bpl, time_limit=1200, print_flag=False):

    if os.path.exists("cegar_num.txt"): os.system("rm cegar_num.txt")

    # ------------------------------------------------------------------------------------------- #
    # ----------------------------------------- translate the ats file ------------------------------------ #
    # ------------------------------------------------------------------------------------------- #
    main_fsm = trans_fsm(ats)



    # ------------------------------------------------------------------------------------------- #
    # ----------------------------------------- trace refinement ------------------------------------ #
    # ------------------------------------------------------------------------------------------- #
    begin = time.time()
    end = begin + 1         # +1 As a judgment that the first run does not timeout
    timeout_flag = True     # determine whether the timeout when returning


    # Get the dir corresponding to the statement
    dir = parsing_bpl(bpl, print_flag=False)

    # first model checking
    check_empty_time = 0
    generalization_time = 0
    check_empty_time_begin = time.time()
    [isEmpty_result, accepted_word_result] = check_empty(main_fsm)
    check_empty_time_end = time.time()
    check_empty_time += (check_empty_time_end - check_empty_time_begin)


    # refinemet and model checking
    refinement_num = 1
    while isEmpty_result == "false" and ((end - begin) < time_limit):

        with open("cegar_num.txt", 'w') as log:
            log.write("++ trace refinement num: " + str(refinement_num))
        # ----------------------------------- new trace_file ----------------------------------------------- #
        if print_flag:
            print(str(refinement_num) + " th - found an error trace: ", accepted_word_result)
            print("\t\t\t\t\t that is, ", translate_albet_to_stat_print(dir, accepted_word_result))
            print("-----------------------------------------------------------------------\n")
        [entry_point, exit_point] = get_while_guard(bpl)
        trace = translate_albet_to_stat_save(dir, accepted_word_result, entry_point, exit_point)


        # -----------------------------------------new automata for trace-------------------------------- #
        generalization_begin = time.time()
        [generalized_result, ats] = generalized_automata(trace, bpl, save_file=False, plot_flag=False, print_flag=False, detail_flag=False)
        generalization_end = time.time()
        generalization_time += (generalization_end - generalization_begin)
        if generalized_result == False:  # found a feasible error trace
            timeout_flag = False
            print("-- generalization time: ", generalization_time)
            print("-- check empty time: ", check_empty_time)
            return False, timeout_flag
        else:
            # ----------------------------------------update the model checking's file------------------------------- #
            counter_example_fsm = trans_fsm(ats)
            main_fsm = intersection(main_fsm, inverse(counter_example_fsm))
            # fsm_show(main_fsm)
            main_fsm.minimize()
            # fsm_show(main_fsm)


        # ------------------------------------------model checking-------------------------------------- #
        check_empty_time_begin = time.time()
        [isEmpty_result, accepted_word_result] = check_empty(main_fsm)
        check_empty_time_end = time.time()
        check_empty_time += (check_empty_time_end - check_empty_time_begin)

        refinement_num += 1
        end = time.time()

    print("-- generalization time: ", generalization_time)
    print("-- check empty time: ", check_empty_time)


    # ------------------------------------------------------------------------------------------- #
    # ----------------------------------------- final result ------------------------------------ #
    # ------------------------------------------------------------------------------------------- #
    if print_flag: print("\n-------------------------------------------")
    if isEmpty_result == "false":   # non-termination
        if os.path.exists("final_result_log.txt"):
            with open("final_result_log.txt", 'a') as log:
                log.write("it is timeout" + " after " + str(refinement_num - 1) + " refinements.\n")
        print(red_none % "it is timeout" + " after " + str(refinement_num - 1) + " refinements.")
        return False, timeout_flag
    elif isEmpty_result == "true":
        if os.path.exists("final_result_log.txt"):
            with open("final_result_log.txt", 'a') as log:
                log.write("congratulation! it takes " + str(refinement_num - 1) + " refinements.\n")
        print("congratulation! it takes " + str(refinement_num - 1) + " refinements.")
        return True, timeout_flag
    else:
        if os.path.exists("final_result_log.txt"):
            with open("final_result_log.txt", 'a') as log:
                log.write("there is something error" + " after " + str(refinement_num - 1) + " refinements.\n")
        print(red_none%"there is something error" + " after " + str(refinement_num - 1) + " refinements.")
        timeout_flag = False
        return "NULL", timeout_flag




if __name__ == "__main__":

    # ---------- coherent program ---------- #
    boogie_file = "../../../ArtifactBenchmark/self-designed/simple_example_ori.bpl"
    # boogie_file = "../../../ArtifactBenchmark/self-designed/assertion_fail_ori.bpl"

    # ------- non-coherent program --------- #
    # boogie_file = "../../../ArtifactBenchmark/self-designed/non_earlyassume_ori.bpl"
    # boogie_file = "../../../ArtifactBenchmark/self-designed/non_memorizing_ori.bpl"
    # boogie_file = "../../../ArtifactBenchmark/self-designed/triple_var_ori.bpl"
    # boogie_file = "../../../ArtifactBenchmark/self-designed/triple_var_2_ori.bpl"
    # boogie_file = "../../../ArtifactBenchmark/other/new_boundary_ori.bpl"

    # ------------------------- test example -------------------------------------#
    # boogie_file = "../../../ArtifactBenchmark/candidate/motivation-example-correct.bpl"
    # boogie_file = "../../../ArtifactBenchmark/svcomp/dll-token-2-incorrect.bpl"
    # boogie_file = "../ProgramGenerator/SLL-5-1-0-correct.bpl"


    bpl = assert_2_assume(boogie_file)
    ats = boogie_to_automata(bpl, save_file=True, print_flag=False)
    trace_refinement(ats, bpl, time_limit=300, print_flag=True)