#!/usr/bin/env python
#-*- coding:utf-8 -*-


from Verifier4UP.src.Parser.assert_2_assume import assert_2_assume
from Verifier4UP.src.ProgramToAutomata.cfg_automata import boogie_to_automata
from Verifier4UP.src.TripleGeneration.triple_info import triple
from Verifier4UP.src.TripleGeneration.collection_triple import collection_info
from Verifier4UP.src.Coherence.Program_Coherence.fix_point_alg import fix_point_alg



def check_infeasible(trace):
    state_map = collection_info(trace)
    if state_map["Q" + str(len(state_map.keys()) - 1)].state == "reject":
        return True
    else:
        return False




def check_coh_program_correct(ats, bpl, save_file=False, print_flag=False):

    info_class = triple
    func = check_infeasible

    if fix_point_alg(ats, bpl, info_class, func, save_file=save_file, print_flag=print_flag):
        if print_flag: print("\nThis coherent program is verified to be correct.")
        return True
    else:
        if print_flag: print("\nThis coherent program is verified to be incorrect.!!!")
        return False



if __name__ == "__main__":

    boogie_file = "../../benchmark/Program/simple_example_ori.bpl"
    # boogie_file = "../../benchmark/Program/assertion_fail_ori.bpl"

    # ------------------------- test example -------------------------------------#

    bpl = assert_2_assume(boogie_file)
    ats = boogie_to_automata(bpl, save_file=True, print_flag=False)
    check_coh_program_correct(ats, bpl, save_file=True, print_flag=True)
