#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
from env_setup import root_path
from Verifier4UP.src.Parser.assert_2_assume import assert_2_assume
from Verifier4UP.src.ProgramToAutomata.auxiliary import automata_to_automata


def boogie_to_automata(bpl, save_file=False, print_flag=False):


    # generate ultimate_ats_file
    env_setting = "export PATH=" + root_path + "UAutomizer-linux:$PATH;"
    os.system(env_setting + "java -jar " + root_path + "Verifier4UP/config/Automata.jar ./program.bpl")

    # transformation
    new_ats = automata_to_automata(bpl, print_flag)


    # save file
    if save_file:
        ats_file = "./program.ats"
        with open(ats_file, "w") as f:
            f.write(new_ats)

    return new_ats




if __name__ == "__main__":


    boogie_file = "../benchmark/Program/simple_example_ori.bpl"

    # ------------------------- test example -------------------------------------#
    boogie_file = "../../../ArtifactBenchmark/candidate/seperation1-correct.bpl"
    boogie_file = "../../../ArtifactBenchmark/benchmark/loop0.bpl"

    new_bpl = assert_2_assume(boogie_file)
    new_ats = boogie_to_automata(new_bpl, save_file=True, print_flag=True)

    # for root, dirs, files in os.walk("../../../ArtifactBenchmark/svcomp/"):
    #     for file in files:
    #         boogie_file = root + file
    #         new_bpl = assert_2_assume(boogie_file)
    #         new_ats = boogie_to_automata(new_bpl, save_file=True, print_flag=False)
