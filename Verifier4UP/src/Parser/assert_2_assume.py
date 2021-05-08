#!/usr/bin/env python
#-*- coding:utf-8 -*-

#
# given a boogie program file(.bpl)， translating assertion into negated assume
#


def assert_2_assume(boogie_file):
    
    new_bpl = ""
    with open(boogie_file, 'r') as f:
        for line in f:
            if "assert" in line:
                line = line.replace("assert", "assume")
                if "==" in line:
                    line = line.replace("==", "!=")
                else:
                    line = line.replace("!=", "==")
            new_bpl = new_bpl + line

    # save file
    bpl_file = "./program.bpl"
    with open(bpl_file, "w") as f:
        f.write(new_bpl)

    return new_bpl
        



if __name__ == "__main__":

    boogie_file = "../benchmark/Program/simple_example_ori.bpl"

    # ------------------------- test example -------------------------------------#

    new_bpl = assert_2_assume(boogie_file)

