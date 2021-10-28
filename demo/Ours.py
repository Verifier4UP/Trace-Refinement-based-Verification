#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
from Verifier4UP.src.VerifyRefinement.log_info import main_run
from Verifier4UP.src.VerifyRefinement.verifyrefinement import verifyrefinement



if __name__ == "__main__":

    boogie_file = "./example/" + sys.argv[1]

    # verifyrefinement(boogie_file, time_limit=1200, save_file=True, print_flag=True)
    main_run(boogie_file, save_file=True, print_flag=True)