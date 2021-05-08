#!/usr/bin/env python
#-*- coding:utf-8 -*-

#
# Give a string corresponding to .tr, parse it and get
# The variable vars that appears
# Function funs that appear
# The corresponding statement list "program_sequence"
# Loop point information "loop_flag"
#


def parsing_trace(trace, print_flag=False):

    trace_lst = trace.split("\n")
    for i in range(len(trace_lst)-1, -1, -1):
        if trace_lst[i] == "":
            del trace_lst[i]



    program_sequence = []   # trace info        [statement1, statement2, ...]
    loop_flag = [0]         # loop point info   [0, 0, 1, 0, 0, ...]
    vars = []               # var info          ["x", "y"]
    funs = [[]]             # func info         [[], ["f"], ["g", "h"], ...], 0-ary，1-ary，2-ary，...


    for line in trace_lst:
        line = line.strip()
        program_sequence.append(line[:line.find(";")])
        # Collect variables and functions
        if ":=" in line:
            if "(" in line:                                             # case: x := f(x)
                left_var = line[: line.find(":=") - 1]
                right_vars = line[line.find("(") + 1: line.find(")")].split(", ")
                fun = line[line.find("=") + 2: line.find("(")]
                # ---------------- vars ------------------ #
                if not (left_var in vars):
                    vars.append(left_var)
                for var in right_vars:
                    if not (var in vars):
                        vars.append(var)
                # ---------------- funs ------------------ #
                for i in range(len(right_vars) + 1):    # start from 0-ary func
                    if i >= len(funs):   # there is not i-ary func
                        funs.append([])
                    if i == len(right_vars):
                        if not (fun in funs[i]):
                            funs[i].append(fun)
            else:                                                       # case: x := y
                left_var = line[: line.find(":=") - 1]
                right_var = line[line.find(":=") + 3: line.find(";")]
                # ---------------- vars ------------------ #
                if not (left_var in vars):
                    vars.append(left_var)
                if not (right_var in vars):
                    vars.append(right_var)
        else:
            if "!" in line:                                             # case: assume(x != y)
                left_var = line[line.find("(") + 1: line.rfind("=") - 2]
                right_var = line[line.rfind("=") + 2: line.find(")")]
                if not (left_var in vars):
                    vars.append(left_var)
                if not (right_var in vars):
                    vars.append(right_var)
            else:                                                       # case: assume(x == y)
                left_var = line[line.find("(") + 1: line.rfind("=") - 2]
                right_var = line[line.rfind("=") + 2: line.find(")")]
                if not (left_var in vars):
                    vars.append(left_var)
                if not (right_var in vars):
                    vars.append(right_var)

        # Collect information about the loop entrance
        if "-Entry" in line:
            loop_flag.append(1)
        elif "-Exit" in line:
            loop_flag.append(-1)
        else:
            loop_flag.append(0)

    if print_flag:
        print("vars: \n", vars)
        print("-------------------------------------------------------")
        print("funs: \n", funs)
        print("-------------------------------------------------------")
        print("trace sequence: \n", program_sequence)
        print("-------------------------------------------------------")
        print("benchmark flag: \n", loop_flag)
        print("-------------------------------------------------------")

    return vars, funs, program_sequence, loop_flag



if __name__ == "__main__":


    trace_file = "../benchmark/Trace/unary_fun.tr"
    trace_file = "../benchmark/Trace/binary_fun.tr"

    # ------------------------- test example -------------------------------------#


    trace = ""
    with open(trace_file, 'r') as f:
        for line in f:
            trace = trace + line
    parsing_trace(trace, print_flag=True)

