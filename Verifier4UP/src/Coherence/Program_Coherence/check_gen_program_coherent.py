#!/usr/bin/env python
#-*- coding:utf-8 -*-

from Verifier4UP.src.Parser.assert_2_assume import assert_2_assume
from Verifier4UP.src.ProgramToAutomata.cfg_automata import boogie_to_automata
from Verifier4UP.src.Coherence.quad_info import quad_info
from Verifier4UP.src.Coherence.Trace_Coherence.check_trace_coherent import check_trace_coherent
from Verifier4UP.src.Coherence.Program_Coherence.fix_point_alg import fix_point_alg



def check_coherence(trace):
    return check_trace_coherent(trace, print_flag=False, detail_flag=False)


def check_gen_program_coherent(ats, bpl, save_file=False, print_flag=False):

    info_class = quad_info
    func = check_coherence

    if fix_point_alg(ats, bpl, info_class, func, save_file=save_file, print_flag=print_flag):
        if print_flag: print("\nThis is a coherent program.")
        return True
    else:
        if print_flag: print("\nThis isn't a coherent program!!!")
        return False


if __name__ == "__main__":

    boogie_file = "../../benchmark/Program/simple_example_ori.bpl"
    # boogie_file = "../../benchmark/Program/non_earlyassume_ori.bpl"
    # boogie_file = "../../benchmark/Program/non_memorizing_ori.bpl"


    # ------------------------- test example -------------------------------------#
    # boogie_file = "../../program.bpl"


    bpl = assert_2_assume(boogie_file)
    ats = boogie_to_automata(bpl, save_file=True, print_flag=False)
    check_gen_program_coherent(ats, bpl, save_file=True, print_flag=True)