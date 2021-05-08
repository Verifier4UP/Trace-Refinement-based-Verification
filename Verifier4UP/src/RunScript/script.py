#!/usr/bin/env python
#-*- coding:utf-8 -*
import os
import sys
BASE_COMMAND_DIR = os.path.dirname(os.path.abspath("../../.."))
sys.path.append(BASE_COMMAND_DIR)
from Verifier4UP.src.RunScript.auxiliary import LoC
from Verifier4UP.src.ULTIMATE.ultimate import ultimate
from Verifier4UP.src.VerifyRefinement.verifyrefinement import verifyrefinement



def run_script(dir, tool, time_threshold, print_flag=False):

    bpl_file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            bpl_file_list.append(root + "/" + file)
    bpl_file_list.sort()


    # --------------------------------------------------------- Ours --------------------------------------------------------------- #
    if tool == "ours":
        with open("./result_ours.txt", "w") as result_file:
            title_tplt = "{:^25}\t{:^10}\t{:^12}\t{:^12}\t{:^12}\t{:^12}\t{:^12}\t{:^12}\t{:^20}"
            data_tplt = "{:25}\t{:^10}\t{:^12}\t{:^12}\t{:^12}\t{:^12}\t{:^12}\t{:^12}\t{:^12}"
            if print_flag: print(title_tplt.format("program", "LoC", "main-result", "main-timecost", "main-trans", "main-sep", "main-Verify", "main-CEGAR", "(#coh)/(#noncoh)"))
            result_file.write(title_tplt.format("program", "LoC", "main-result", "main-timecost", "main-trans", "main-sep", "main-Verify", "main-CEGAR", "(#coh)/(#noncoh)") + "\n")
            for boogie_file in bpl_file_list:
                loc = LoC(boogie_file)
                [transformantion_time, coherence_num, noncoherence_num, seperation_time, Verification_time, non_coherence_refined_num, nonVerification_time, total_time, main_result] = verifyrefinement(boogie_file, time_limit=time_threshold, save_file=False, print_flag=False)
                if print_flag: print(data_tplt.format(boogie_file[boogie_file.rfind("/") + 1:], loc,
                                       main_result, total_time,
                                       transformantion_time, seperation_time,
                                       Verification_time, nonVerification_time,
                                       str(coherence_num) + "\\" + str(noncoherence_num) + "(" + non_coherence_refined_num + ")"))
                result_file.write(data_tplt.format(boogie_file[boogie_file.rfind("/") + 1:], loc,
                                       main_result, total_time,
                                       transformantion_time, seperation_time,
                                       Verification_time, nonVerification_time,
                                       str(coherence_num) + "\\" + str(noncoherence_num) + "(" + non_coherence_refined_num + ")")
                                       + "\n")


    # ------------------------------------------------------ Automizer ------------------------------------------------------------- #
    elif tool == "ultimate":
        with open("./result_ultimate.txt", "w") as result_file:
            title_tplt = "{:^35}\t{:^10}\t{:^12}\t{:^12}\t{:^12}"
            data_tplt = "{:35}\t{:^10}\t{:^12}\t{:^12}\t{:^12}"
            if print_flag: print(title_tplt.format("program", "LoC", "UA-result", "UA-timecost", "UA-iteration"))
            result_file.write(title_tplt.format("program", "LoC", "UA-result", "UA-timecost", "UA-iteration") + "\n")
            for boogie_file in bpl_file_list:
                loc = LoC(boogie_file)
                [Iteration_num, timecost, result] = ultimate(boogie_file, time_limit=time_threshold, print_flag=False)
                if print_flag: print(data_tplt.format(boogie_file[boogie_file.rfind("/") + 1:], loc,
                                       Iteration_num, timecost, result))
                result_file.write(data_tplt.format(boogie_file[boogie_file.rfind("/") + 1:], loc,
                                       result, timecost, Iteration_num) + "\n")



if __name__ == "__main__":

    dir = sys.argv[1]
    tool = sys.argv[2]
    time_threshold = int(sys.argv[3])

    # dir = "../ArtifactBenchmark/svcomp"
    # dir = "../ArtifactBenchmark/self-designed"
    # dir = "../ArtifactBenchmark/error_test"
    # tool = "ours"
    # tool = "ultimate"
    # tool = "both"
    # time_threshold = 30

    run_script(dir, tool, time_threshold, print_flag=False)
