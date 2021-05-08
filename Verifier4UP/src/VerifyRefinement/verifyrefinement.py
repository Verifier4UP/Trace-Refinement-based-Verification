#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import copy
from env_setup import root_path


def verifyrefinement(boogie_file, time_limit, save_file=False, print_flag=False):


    # -------------------------------------- setup -------------------------------------------------------- #
    command_timelimit = "timeout " + str(time_limit) + " "
    run_commamd = "python3 " + root_path + "Verifier4UP/src/VerifyRefinement/log_info.py " + boogie_file + " " + str(save_file) + " " + str(print_flag)


    # -------------------------------------- execution -------------------------------------------------------- #
    result = os.popen(command_timelimit + run_commamd).read()
    if print_flag: print(result)


    # -------------------------------------- output filter -------------------------------------------------------- #
    transformantion_time = 0
    coherence_num = 0
    noncoherence_num = 0
    seperation_time = 0
    Verification_time = 0
    non_coherence_refined_num = []
    Check_time = 0
    total_time = time_limit
    reason = "timeout"

    with open("./final_result_log.txt", 'r') as log:
        for line in log:
            if "++ transformantion time" in line:
                transformantion_time = float(line[line.find(":") + 2:line.rfind("s")])

            elif "coherent:" in line and not ("non-coherent:" in line):
                coherence_num = line.count("ats")

            elif "non-coherent:" in line:
                noncoherence_num = line.count("ats")
                non_coherence_refined_num = ['0'] * noncoherence_num
                non_coherence_refined_idx = 0

            elif "++ seperation time" in line:
                seperation_time = float(line[line.find(":") + 2:line.rfind("s")])

            elif "++ verification time" in line:
                Verification_time = float(line[line.find(":") + 2:line.rfind("s")])

            elif "refinements." in line:
                non_coherence_refined_num[non_coherence_refined_idx] = line.split(" ")[-2]
                non_coherence_refined_idx += 1

            elif "++ trace refinement time" in line:
                Check_time = float(line[line.find(":") + 2:line.rfind("s")])

            elif "the whole process takes" in line:
                total_time = float(line.split(" ")[-1][0:-3])

            elif "The program is" in line:
                reason = line.split(" ")[-1][0:-1]


    if ("timeout" in reason or "incorrect" in reason) and os.path.exists("./cegar_num.txt"):
        with open("./cegar_num.txt", 'r') as cegar_f:
            for line_num in cegar_f:
                if "++ trace refinement num" in line_num:
                    non_coherence_refined_num[non_coherence_refined_idx] = line_num[line_num.find(":") + 2:]
    tmp = copy.deepcopy(non_coherence_refined_num)
    non_coherence_refined_num = "-"
    for num in tmp:
        if num == "0":
            break
        else:
            non_coherence_refined_num += num + "-"
    non_coherence_refined_num = non_coherence_refined_num

    if print_flag: print("final result: ",
                         transformantion_time,
                         coherence_num,
                         noncoherence_num,
                         seperation_time,
                         Verification_time,
                         non_coherence_refined_num,
                         Check_time,
                         total_time,
                         reason)


    return transformantion_time, coherence_num, noncoherence_num, seperation_time, Verification_time, non_coherence_refined_num, Check_time, total_time, reason