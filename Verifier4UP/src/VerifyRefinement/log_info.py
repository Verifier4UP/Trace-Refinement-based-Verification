#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
import time
BASE_COMMAND_DIR = os.path.dirname(os.path.abspath("../../.."))
sys.path.append(BASE_COMMAND_DIR)
from Verifier4UP.src.Parser.color import red_none, blue_none, purple_none
from Verifier4UP.src.Parser.assert_2_assume import assert_2_assume
from Verifier4UP.src.Parser.automata2Boogie import automata2Boogie
from Verifier4UP.src.CEGAR.cegar import trace_refinement
# from Verifier4UP.src.CEGAR.cegar_ultimate import trace_refinement
from Verifier4UP.src.ProgramPartition.pro_partition import partition
from Verifier4UP.src.ProgramToAutomata.cfg_automata import boogie_to_automata
from Verifier4UP.src.Coherence.Program_Coherence.check_coh_program_correct import check_coh_program_correct
from Verifier4UP.src.ULTIMATE.ultimate import ultimate

# trace_refinement_mode = "ULTIMATE"
trace_refinement_mode = "Ours"


def check_file_exist(suffix):
    files = os.listdir("./")
    for file in files:
        if suffix in file:
            return True
    return False



def Verification_process(coherent_automata_file, bpl, print_flag):
    Verify_begin = time.time()

    verification_result = True
    reason = "correct"

    for file in coherent_automata_file.keys():
        ats = coherent_automata_file[file]
        result = check_coh_program_correct(ats, bpl, save_file=False, print_flag=False)
        if result == False:
            if print_flag: print(blue_none % file + " is verified to be incorrect\n")
            verification_result = False
            reason = "incorrect"
            break
        else:
            if print_flag: print(blue_none % file + " is verified to be correct\n")

    Verify_end = time.time()
    Verification_time = Verify_end - Verify_begin

    return verification_result, Verification_time, reason


def CEGAR_process(non_coherent_automata_file, bpl, print_flag):
    CEGAR_begin = time.time()

    CEGAR_result = True
    reason = "correct"

    for file in non_coherent_automata_file.keys():
        ats = non_coherent_automata_file[file]

        [result, timeout_flag] = trace_refinement(ats, bpl, time_limit=86400, print_flag=False)
        if result == True:  # verified successful
            if print_flag: print(purple_none % file + " is checked to be correct\n")
            CEGAR_result = True
            reason = "correct"
        elif result == "NULL":  # error
            if print_flag: print(purple_none % file + " can't be checked due to certain errors\n")
            CEGAR_result = False
            reason = "error"
            break
        elif timeout_flag:  # timeout
            if print_flag: print(purple_none % file + " is checked to be unknown due to the time limit\n")
            CEGAR_result = False
            reason = "timeout"
            break
        else:  # counter-example
            if print_flag: print(purple_none % file + " is checked to find a counter-example\n")
            CEGAR_result = False
            reason = "incorrect"
            break

    CEGAR_end = time.time()
    Check_time = CEGAR_end - CEGAR_begin

    return CEGAR_result, reason, Check_time


def ULTIMATE_process(non_coherent_automata_file, bpl, print_flag):
    CEGAR_begin = time.time()

    transform_time = 0
    CEGAR_result = True
    reason = "correct"

    for file in non_coherent_automata_file.keys():
        ats = non_coherent_automata_file[file]
        transform_begin = time.time()
        ats_bpl = file[:file.rfind(".")] + ".bpl"
        automata2Boogie(bpl, ats, ats_bpl)
        transform_end = time.time()
        transform_time += transform_end - transform_begin

        [Iteration_num, timecost, reason] = ultimate(ats_bpl, time_limit=86400, print_flag=False)
        with open("final_result_log.txt", 'a') as log:
            log.write("It takes " + str(Iteration_num) + " refinements.\n")

        print("It takes " + str(Iteration_num) + " refinements.")
        if reason == "correct":
            if print_flag: print(purple_none % file + " is checked to be correct\n")
            CEGAR_result = True
        elif reason == "incorrect":
            if print_flag: print(purple_none % file + " is checked to find a counter-example\n")
            CEGAR_result = False
            break
        elif reason == "error":
            if print_flag: print(purple_none % file + " can't be checked due to certain errors\n")
            CEGAR_result = False
            break
        elif reason == "timeout":
            if print_flag: print(purple_none % file + " is checked to be unknown due to the time limit\n")
            CEGAR_result = False
            break

    CEGAR_end = time.time()
    Check_time = CEGAR_end - CEGAR_begin - transform_time

    return CEGAR_result, reason, Check_time


def main_run(boogie_file, save_file=False, print_flag=False):


    # begin_time = time.time()
    transform_time = 0
    seperation_time = 0
    Verification_time = 0
    Check_time = 0

    pure_verification = False
    pure_trace_refinement = False
    auto = True


    # ----------------------------------clean up---------------------------------- #
    if check_file_exist(".tr"): os.system("rm *.tr")
    if check_file_exist(".ats"): os.system("rm *.ats")
    if check_file_exist(".bpl"): os.system("rm *.bpl")
    if os.path.exists("final_result_log.txt"): os.system("rm final_result_log.txt")


    # ------------------------------- 0. assert transofrmation ------------------------------- #
    # if print_flag: print(red_none % "step1: transforming program into automata...")
    transform_begin = time.time()
    new_bpl = assert_2_assume(boogie_file)

    # ------------------------------ 1.program -> automata ----------------------------- #
    new_ats = boogie_to_automata(new_bpl, save_file=save_file, print_flag=False)
    transform_end = time.time()
    transform_time = transform_end - transform_begin
    # if print_flag: print("++ transformantion time: " + str('%.3f' % (transform_time)) + "s.\nfinished.\n\n")
    with open("final_result_log.txt", 'a') as log:
        log.write("++ transformantion time: " + str('%.3f' % (transform_time)) + "s.\n\n")


    # ----------------------------------- 2.partition ------------------------------- #
    if print_flag: print(red_none % "step: separating program into coh/non-coh...")
    seperation_begin = time.time()
    if auto:
        if print_flag: print(red_none % "Mode: auto")
        [coherent_automata_file, non_coherent_automata_file] = partition(new_ats, new_bpl, save_file=save_file, print_flag=False)
    if pure_verification:
        if print_flag: print(red_none % "Mode: pure_verification")
        # program_ats = ""
        # with open("./program.ats", "r") as f:
        #     for line in f:
        #         program_ats = program_ats + line
        program_ats = new_ats
        coherent_automata_file = {"./program.ats": program_ats}
        non_coherent_automata_file = {}
    if pure_trace_refinement:
        if print_flag: print(red_none % "Mode: pure_trace_refinement")
        coherent_automata_file = {}
        # program_ats = ""
        # with open("./program.ats", "r") as f:
        #     for line in f:
        #         program_ats = program_ats + line
        program_ats = new_ats
        non_coherent_automata_file = {"./program.ats": program_ats}

    seperation_end = time.time()
    seperation_time = seperation_end - seperation_begin
    coherence_num = len(coherent_automata_file.keys())
    noncoherence_num = len(non_coherent_automata_file.keys())


    if print_flag:
        print(blue_none % "coherent: ", str(list(coherent_automata_file.keys())))
        print(purple_none % "non-coherent: ", str(list(non_coherent_automata_file.keys())))
        print("++ seperation time: " + str('%.3f' % (seperation_time)) + "s.\nfinished.\n\n")

    with open("final_result_log.txt", 'a') as log:
        log.write("coherent: " + str(list(coherent_automata_file.keys())) + "\n")
        log.write("non-coherent: " + str(list(non_coherent_automata_file.keys())) + "\n")
        log.write("++ seperation time: " + str('%.3f' % (seperation_time)) + "s.\n\n")




    # ------------------------------- 3.verification -------------------------- #
    if print_flag: print(red_none % "step: Verification & Trace Refinement...")
    verification_result = True
    CEGAR_result = True

    # verification first
    if print_flag: print("----------------------------------------\n" + blue_none % "\t\tVerification: ")

    if coherence_num != 0:

        [verification_result, Verification_time, reason] = Verification_process(coherent_automata_file, new_bpl,
                                                                        print_flag=print_flag)
        if print_flag: print("++ verification time: ", str('%.3f' % Verification_time) + "s.")
        with open("final_result_log.txt", 'a') as log:
            log.write("++ verification time: " + str('%.3f' % Verification_time) + "s." + "\n")


        # then trace_refinement
        if print_flag: print("----------------------------------------\n" + purple_none % "\t\tTrace Refinement: ")

        if verification_result and noncoherence_num != 0:  # Verification passed，and trace_refinement is not empty

            if trace_refinement_mode == "ULTIMATE":
                [CEGAR_result, reason, Check_time] = ULTIMATE_process(non_coherent_automata_file, new_bpl,
                                                                   print_flag=print_flag)
            else:
                [CEGAR_result, reason, Check_time] = CEGAR_process(non_coherent_automata_file, new_bpl,
                                                                print_flag=print_flag)
            if print_flag: print("++ trace refinement time: ", str('%.3f' % Check_time) + "s.")
            with open("final_result_log.txt", 'a') as log:
                log.write("++ trace refinement time: " + str('%.3f' % Check_time) + "s." + "\n\n")


    else:  # trace_refinment
        if print_flag: print("----------------------------------------\n" + purple_none % "\t\tTrace Refinement: ")

        if trace_refinement_mode == "ULTIMATE":
            [CEGAR_result, reason, Check_time] = ULTIMATE_process(non_coherent_automata_file, new_bpl,
                                                                  print_flag=print_flag)
        else:
            [CEGAR_result, reason, Check_time] = CEGAR_process(non_coherent_automata_file, new_bpl,
                                                               print_flag=print_flag)
        if print_flag: print("++ trace refinement time: ", str('%.3f' % Check_time) + "s.")
        with open("final_result_log.txt", 'a') as log:
            log.write("++ trace refinement time: " + str('%.3f' % Check_time) + "s." + "\n\n")

    if print_flag: print("----------------------------------------\nfinished.\n")

    # ------------------------------- 4.final result -------------------------- #
    if print_flag: print(red_none % "\n----------------------------------------\n----------------------------------------")
    if verification_result and CEGAR_result:
        if print_flag: print("The program is verified/checked to be " + red_none % "correct")
        with open("final_result_log.txt", 'a') as log:
            log.write("\nThe program is verified/checked to be correct\n")
    elif verification_result and not CEGAR_result:
        if reason != "error":
            if print_flag: print(
                "The program is checked to be " + red_none % "incorrect.")
            with open("final_result_log.txt", 'a') as log:
                log.write("\nThe program is checked to be incorrect\n")
        else:
            if print_flag: print(
                "The program is checked while " + red_none % "error")
            with open("final_result_log.txt", 'a') as log:
                log.write("\nThe program is checked while error\n")
    else:
        if print_flag: print(
            "The program is verified to be " + red_none % "incorrect.")
        with open("final_result_log.txt", 'a') as log:
            log.write("\nThe program is checked to be incorrect\n")

    # end_time = time.time()
    # total_time = end_time - begin_time
    total_time = transform_time + seperation_time + Verification_time + Check_time
    if print_flag: print("the whole process takes " + red_none % (str('%.3f' % total_time)) + "s.")
    with open("final_result_log.txt", 'a') as log:
        log.write("the whole process takes " + str('%.3f' % total_time) + "s.\n\n")


if __name__ == "__main__":

    boogie_file = sys.argv[1]
    save_file = sys.argv[2]
    print_flag = sys.argv[3]

    if save_file == "False":
        save_file = False
    elif save_file == "True":
        save_file = True
    if print_flag == "False":
        print_flag = False
    elif print_flag == "True":
        print_flag = True

    main_run(boogie_file, save_file=save_file, print_flag=print_flag)
