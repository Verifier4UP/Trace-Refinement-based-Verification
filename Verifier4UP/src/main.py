#!/usr/bin/env python
#-*- coding:utf-8 -*-
from Verifier4UP.src.VerifyRefinement.log_info import main_run
from Verifier4UP.src.VerifyRefinement.verifyrefinement import verifyrefinement


if __name__ == "__main__":



    # --------------benchmark--------------- #
    # boogie_file = "../../ArtifactBenchmark/benchmark/benchmark1.bpl"

    # ----------------svcomp---------------- #
    # boogie_file = "../../ArtifactBenchmark/svcomp/benchmark1.bpl"

    # -----------------other---------------- #
    # boogie_file = "../../ArtifactBenchmark/other/self-construction/simple_example_correct.bpl"

    # -----------------demo----------------- #
    # boogie_file = "../../demo/example/moti-example.bpl"

    boogie_file = "../../ArtifactBenchmark/benchmark/benchmark1.bpl"


    # verifyrefinement(boogie_file, time_limit=60, save_file=True, print_flag=True)
    main_run(boogie_file, save_file=True, print_flag=True)