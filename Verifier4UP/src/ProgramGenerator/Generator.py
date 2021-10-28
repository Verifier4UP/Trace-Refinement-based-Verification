#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from Verifier4UP.src.ProgramGenerator.SLL import generator_sll
from Verifier4UP.src.ProgramGenerator.TREE import generator_tree
from Verifier4UP.src.ProgramGenerator.BENCHMARK import generator_benchmark

if __name__ == "__main__":

    SLL_flag = False
    TREE_flag = False
    BENCHMARK_flag = True

    if SLL_flag:
        sll_length = [3, 4, 5, 6, 7, 8, 9, 10]
        value_range = 2
        mutation_num = [0, 1, 2, 3, 4, 5]

        if not (os.path.exists("../../../ArtifactBenchmark/SLL")):
            os.system("mkdir ../../../ArtifactBenchmark/SLL")
        else:
            os.system("rm -r ../../../ArtifactBenchmark/SLL")
            os.system("mkdir ../../../ArtifactBenchmark/SLL")


        for sl in sll_length:
            for mn in mutation_num:
                print("\n-------------")
                generator_sll(sl, value_range, mn, print_flag=True)
                os.system("mv *.bpl ../../../ArtifactBenchmark/SLL/")

    if TREE_flag:
        max_nodes = [5, 10, 15, 20]
        value_range = 2

        if not (os.path.exists("../../../ArtifactBenchmark/TREE")):
            os.system("mkdir ../../../ArtifactBenchmark/TREE")
        else:
            os.system("rm -r ../../../ArtifactBenchmark/TREE")
            os.system("mkdir ../../../ArtifactBenchmark/TREE")

        for mn in max_nodes:
            print("\n-------------")
            generator_tree(mn, value_range, print_flag=True)
            os.system("mv *.bpl ../../../ArtifactBenchmark/TREE/")


    if BENCHMARK_flag:
        if not (os.path.exists("../../../ArtifactBenchmark/benchmark")):
            os.system("mkdir ../../../ArtifactBenchmark/benchmark")
        else:
            os.system("rm -r ../../../ArtifactBenchmark/benchmark")
            os.system("mkdir ../../../ArtifactBenchmark/benchmark")
        i = 0
        correctness_lst = []
        incorrectness_num = 0
        while i < 50:
            correctness = generator_benchmark()
            if (not correctness) and incorrectness_num == 25:
                print("saturation at" + str(i))
                os.system("rm benchmark-program.bpl")
                continue
            else:
                correctness_lst.append(correctness)
                if not correctness: incorrectness_num += 1
                os.system("mv benchmark-program.bpl benchmark" + str(i) + ".bpl")
                i += 1
        os.system("mv *.bpl ../../../ArtifactBenchmark/benchmark/")
        print(correctness_lst[0: 10])
        print(correctness_lst[10: 20])
        print(correctness_lst[20: 30])
        print(correctness_lst[30: 40])
        print(correctness_lst[40: 50])