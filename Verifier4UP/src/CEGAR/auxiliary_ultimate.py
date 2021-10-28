#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from Verifier4UP.src.Parser.parsing_trace import parsing_trace
from env_setup import root_path

# ----------------------------------------------------- auxiliary func ---------------------------------------- #
# generate the format of intersection for  Automata Libaray
def intersection(n):
    if n == 0:
        intersec = "FiniteAutomaton intersecNfa = FSM;\n"
    else:
        intersec = "difference(FSM, M1)"
        for i in range(n + 1):
            if i > 1:
                intersec = "difference(" + intersec + ", M" + str(i) + ")"
        intersec = "FiniteAutomaton intersecNfa = " + intersec + ";\n"
    return intersec


# translating the alphabet sequence into the statement sequence
def translate_albet_to_stat_save(dir, alphabet_seq, entry_point, exit_point):

    reverse_dir = {}
    for key in dir.keys():
        reverse_dir[dir[key]] = key

    word = alphabet_seq.split(" ")
    trace = ""
    for i in word:
        if reverse_dir[i] in entry_point:
            trace = trace + reverse_dir[i] + "; -Entry\n"
        elif reverse_dir[i] in exit_point:
            trace = trace + reverse_dir[i] + "; -Exit\n"
        else:
            trace = trace + reverse_dir[i] + ";\n"

    return trace

def translate_albet_to_stat_print(dir, alphabet_seq):

    reverse_dir = {}
    for key in dir.keys():
        reverse_dir[dir[key]] = key

    trace = ""
    word = alphabet_seq.split(" ")
    for i in word:
        trace += reverse_dir[i] + "; "
    return trace[:-2]


# translating the statement sequence into the alphabet sequence
def translate_stat_to_albet(dir, file):
    program_sequence = parsing_trace(file, print_flag=False)[2]
    word = ""
    for i in range(len(program_sequence)):
        word = word + dir[program_sequence[i]] + " "
    print(word)


# ----------------------------------------------------- other func ---------------------------------------- #
# modify .ats file
def update_automata(main_automata, trace_automata, trace_num):

    alphabet_list = ""
    remained_one = ""
    with open(main_automata, "r") as main_fsm:
        for line in main_fsm:
            if "alphabet" in line:  # unify all automata's alphabet
                alphabet_list = line
                remained_one += line
            elif "intersecNfa" in line:
                break
            else:                   # get the last automaton
                remained_one += line


    # add new automata
    with open(main_automata, "w") as main_fsm:
        for line in remained_one:
            main_fsm.write(line)
        main_fsm.write("\n")
        trace_automata_lst = trace_automata.split("\n")
        for line in trace_automata_lst:
            if "FiniteAutomaton" in line:
                main_fsm.write("FiniteAutomaton M" + str(trace_num) + "= (\n")
            elif "alphabet" in line:
                main_fsm.write(alphabet_list)
            else:
                main_fsm.write(line + "\n")
        main_fsm.write("\n" + intersection(trace_num))
        main_fsm.write("print(isEmpty(intersecNfa));\n")
        main_fsm.write("Word word = getAcceptedWord(intersecNfa);\n")
        main_fsm.write("print(word);")


# call ULTIMATE to do model checking
def check_empty(file, ultimate_info=False):

    # -------------------------------------- setup -------------------------------------------------------- #
    env_setting = "export PATH=" + root_path + "UAutomizer-linux:$PATH;"
    ultimate_commamd = " Ultimate -tc " + root_path + "Verifier4UP/config/AutomataScriptInterpreter.xml -i " + file
    result = os.popen(env_setting + ultimate_commamd + " 2>&1").read()


    # -------------------------------------- output filter -------------------------------------------------------- #
    isEmpty_flag = False
    isEmpty_result = ""
    accepted_word_flag = False
    accepted_word_result = ""

    result = result.split("\n")

    flag = False
    for line in result:

        if ultimate_info:
            # ----------------------------- actual output -------------------------#
            if "RESULT: Ultimate could not prove your program" in line:
                flag = False
            if flag:
                print(line)
            if " --- Results ---" in line:
                print("-----------------------------------------------------------------------")
                flag = True

        # ----------------------------- parser output -------------------------#
        if isEmpty_flag == True:
            isEmpty_result = line
            isEmpty_flag = False
        if "- GenericResultAtElement" in line and "print(isEmpty(intersecNfa))" in line:
            isEmpty_flag = True
        if accepted_word_flag == True:
            accepted_word_result = line
            accepted_word_flag = False
        if "- GenericResultAtElement" in line and "print(word)" in line:
            accepted_word_flag = True


    isEmpty_result = isEmpty_result.strip()
    if "false" in isEmpty_result:
        trace = ""
        accepted_word_result = accepted_word_result.strip()
        accepted_word_result = accepted_word_result.split('\"')
        for item in accepted_word_result:
            trace = trace + item
        accepted_word_result = trace

    return isEmpty_result, accepted_word_result



if __name__ == "__main__":
   pass