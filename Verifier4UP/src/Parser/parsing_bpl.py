#!/usr/bin/env python
#-*- coding:utf-8 -*-
from Verifier4UP.src.Parser.assert_2_assume import assert_2_assume

#
# Give a string corresponding to .bpl and parse it to get
# A mapping dictionary between a statment and a letter {statment --> Aa/Ba/Cb/...}
# Currently supports up to (26*26)/(26+26) different statements
#


def parsing_bpl(bpl, print_flag=False):

    bpl_lst = bpl.split("\n")

    dir = {}
    # alphabet_idx_1 = ord('A')  # at most 26 different characters
    # alphabet_idx_2 = ord('a')  # at most 26 different characters
    alphabet_idx_A = ord('A')  # at most 26 different characters
    alphabet_idx_a = ord('a')  # at most 26 different characters
    alphabet_idx = alphabet_idx_A

    for line in bpl_lst:
        line = line.strip()
        if "if" in line or "while" in line:
            left_var = line[line.find("(") + 1:line.rfind("=") - 2]
            right_var = line[line.rfind("=") + 2:line.find(")")]
            statement1 = "assume(" + left_var + " != " + right_var + ")"
            statement2 = "assume(" + left_var + " == " + right_var + ")"
            if not (statement1 in dir.keys()):
                dir[statement1] = chr(alphabet_idx)
                if chr(alphabet_idx) == "Z":
                    alphabet_idx = alphabet_idx_a
                else:
                    alphabet_idx += 1
                # dir[statement1] = chr(alphabet_idx_1) + chr(alphabet_idx_2)
                # if chr(alphabet_idx_2) == "z":
                #     alphabet_idx_1 += 1
                #     alphabet_idx_2 = ord('a')
                # else:
                #     alphabet_idx_2 += 1
            if not (statement2 in dir.keys()):
                dir[statement2] = chr(alphabet_idx)
                if chr(alphabet_idx) == "Z":
                    alphabet_idx = alphabet_idx_a
                else:
                    alphabet_idx += 1
                # dir[statement2] = chr(alphabet_idx_1) + chr(alphabet_idx_2)
                # if chr(alphabet_idx_2) == "z":
                #     alphabet_idx_1 += 1
                #     alphabet_idx_2 = ord('a')
                # else:
                #     alphabet_idx_2 += 1
        elif "assert" in line:
            statement = "assume" + line[line.find("("):-1]
            if not (statement in dir.keys()):
                dir[statement] = chr(alphabet_idx)
                if chr(alphabet_idx) == "Z":
                    alphabet_idx = alphabet_idx_a
                else:
                    alphabet_idx += 1
                # dir[statement] =chr(alphabet_idx_1) + chr(alphabet_idx_2)
                # if chr(alphabet_idx_2) == "z":
                #     alphabet_idx_1 += 1
                #     alphabet_idx_2 = ord('a')
                # else:
                #     alphabet_idx_2 += 1
        elif (":=" in line) or ("!=" in line) or ("==" in line):
            statement = line[:line.find(";")]
            if not (statement in dir.keys()):
                dir[statement] = chr(alphabet_idx)
                if chr(alphabet_idx) == "Z":
                    alphabet_idx = alphabet_idx_a
                else:
                    alphabet_idx += 1
                # dir[statement] = chr(alphabet_idx_1) + chr(alphabet_idx_2)
                # if chr(alphabet_idx_2) == "z":
                #     alphabet_idx_1 += 1
                #     alphabet_idx_2 = ord('a')
                # else:
                #     alphabet_idx_2 += 1
    if print_flag:
        print_dir = sorted(dir.items(), key=lambda x: x[1], reverse=False)
        for item in print_dir:
            print(item[1], ":", item[0])
    return dir


if __name__ == "__main__":

    boogie_file = "../benchmark/Program/simple_example_ori.bpl"


    # ------------------------- test example -------------------------------------#


    new_bpl = assert_2_assume(boogie_file)
    parsing_bpl(new_bpl, print_flag=True)