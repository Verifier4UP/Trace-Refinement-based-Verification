#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import time
from env_setup import root_path

def ultimate(bpl_file, time_limit=1200, print_flag=False):

    # -------------------------------------- setup -------------------------------------------------------- #
    command_timelimit = "timeout " + str(time_limit) + " "
    env_setting = "export PATH=" + root_path + "UAutomizer-linux:$PATH;"
    ultimate_commamd = "Ultimate -tc " + root_path + "Verifier4UP/config/AutomizerBpl.xml -i " + bpl_file



    # -------------------------------------- execution -------------------------------------------------------- #
    begin = time.time()
    result = os.popen(env_setting + command_timelimit + ultimate_commamd).read()
    end = time.time()


    # -------------------------------------- output filter -------------------------------------------------------- #
    result = result.split("\n")
    flag = False
    ultimate_result = "<ultimate's call failed>"
    Iteration_num = 0
    for line in result:
        if "Received shutdown request..." in line:
            flag = False
        if flag:
            if print_flag: print(line)

            if "Ultimate could not prove your program: Toolchain returned no result." in line:
                ultimate_result = "error"
            elif "Ultimate proved your program to be correct!" in line:
                ultimate_result = "correct"
            elif "Ultimate proved your program to be incorrect!" in line:
                ultimate_result = "incorrect"
            elif "Completed graceful shutdown" in line:
                ultimate_result = "timeout"

        if "=== Iteration" in line:
            Iteration_num += 1
            if print_flag: print(line)
        if "#######################  End [Toolchain 1] ##" in line:
            flag = True
            if print_flag: print("\n")

    timecost = end - begin
    if print_flag: print("TIMECOST:", str(timecost))

    return Iteration_num, '%.3f' % timecost, ultimate_result





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
    # candidate
    # boogie_file = "../../../ArtifactBenchmark/candidate/motivation-example-correct.bpl"

    # benchmark
    # boogie_file = "../../../ArtifactBenchmark/benchmark/benchmark1.bpl"

    # SLL & TREE
    # boogie_file = "../ProgramGenerator/SLL-5-1-0-correct.bpl"
    # boogie_file = "../ProgramGenerator/TREE-6-1-correct.bpl"

    # svcomp
    # boogie_file = "../../../ArtifactBenchmark/svcomp/array3-correct.bpl"




    [Iteration_num, timecost, ultimate_result] = ultimate(boogie_file, time_limit=1200, print_flag=True)
    print("\n\n----------------------------------------\n"
          "----------------------------------------\n"
          "The program is verified/checked to be " + ultimate_result + "\n"
          "the whole process takes " + str(timecost) + "s in " + str(Iteration_num)+ " refinements.")

