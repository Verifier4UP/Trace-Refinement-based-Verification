#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
from Verifier4UP.src.ULTIMATE.ultimate import ultimate

if __name__ == "__main__":

    boogie_file = "./example/" + sys.argv[1]


    [Iteration_num, timecost, ultimate_result] = ultimate(boogie_file, time_limit=1200, print_flag=True)
    print("\n\n----------------------------------------\n"
          "----------------------------------------\n"
          "The program is verified/checked to be " + ultimate_result + "\n"
          "the whole process takes " + str(timecost) + "s in " + str(Iteration_num) + " refinements.")