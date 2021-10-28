#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time
import copy
from tarjan import tarjan
from Verifier4UP.src.Parser.assert_2_assume import assert_2_assume
from Verifier4UP.src.ProgramToAutomata.cfg_automata import boogie_to_automata
from Verifier4UP.src.Coherence.Program_Coherence.check_gen_program_coherent import check_gen_program_coherent

def check_SCC(SCC, node):
    for item in SCC:
        if node in item:
            return len(item), item


def partition(ats, bpl, save_file=False, print_flag=False):

    query_time = 0

    ats_lst = ats.split("\n")
    bpl_lst = bpl.split("\n")

    # -------------------------------------- get the transition of each state according to ats file ---------------------------- #
    # for example: degree_dir = {"q0": [["A", "q1"]], "q1"： [["B", "q2"], ["C", "q3"]], ....}
    #              tarjan_dir = {"q0": ["q1"], "q1": ["q2", "q3"], ...}
    #              all_trans = [["q0", "A", "q1"], ["q1", "B", "q2"], ...]
    flag = False
    degree_dir = {}
    tarjan_dir = {}
    all_trans = []
    for line in ats_lst:
        if flag:
            if "}" in line:
                tarjan_dir["q"+str(len(tarjan_dir))] = []
                break
            line = line.strip()[1:-1].split(" ")
            all_trans.append([line[0], line[1], line[2]])
            if line[0] in degree_dir.keys():
                degree_dir[line[0]].append([line[1], line[2]])
                tarjan_dir[line[0]].append(line[2])
            else:
                degree_dir[line[0]] = [[line[1], line[2]]]
                tarjan_dir[line[0]] = [line[2]]
        if "transition" in line:
            flag = True


    # --------------------------------------- calculate SCC according to tarjan_dir ------------------------------- #
    SCC = tarjan(tarjan_dir)
    if print_flag: print("SCC:\n", SCC, "\n-------------------------\n")




    # --------------------------------------------------- partition ----------------------------------------- #
    final_result = {}

    # Each state set, its corresponding transition, the current last selected state should be saved separately
    work_list = ["q0"]
    work_list_trans = {"q0": []}
    work_list_choice = {"q0": "q0"}


    while len(work_list) != 0:

        current_set = work_list.pop()
        current_trans = work_list_trans[current_set]
        current_choice = work_list_choice[current_set]
        del work_list_trans[current_set]
        del work_list_choice[current_set]

        if not (current_choice in degree_dir.keys()):    # reach exit

            if print_flag: print("new trans set: ", current_trans)
            final_result[current_set] = current_trans

        elif len(degree_dir[current_choice]) == 1:       # sequential
            source_node = current_choice
            action = degree_dir[current_choice][0][0]
            sink_node = degree_dir[current_choice][0][1]
            trans = [source_node, action, sink_node]

            new_set = current_set + " " + sink_node
            new_trans = current_trans + [trans]
            new_choice = sink_node

            work_list.append(new_set)
            work_list_trans[new_set] = new_trans
            work_list_choice[new_set] = new_choice

        elif len(degree_dir[current_choice]) == 2:          # if_else / while

            if check_SCC(SCC, current_choice)[0] == 1:                # if_else

                source_node = current_choice

                # -------------------------- copy branch ----------------------------- #
                action1 = degree_dir[current_choice][0][0]
                sink_node1 = degree_dir[current_choice][0][1]
                trans1 = [source_node, action1, sink_node1]

                new_set1 = current_set + " " + sink_node1
                new_trans1 = current_trans + [trans1]
                new_choice1 = sink_node1

                work_list.append(new_set1)
                work_list_trans[new_set1] = new_trans1
                work_list_choice[new_set1] = new_choice1

                # -------------------------- copy branch ----------------------------- #
                action2 = degree_dir[current_choice][1][0]
                sink_node2 = degree_dir[current_choice][1][1]
                trans2 = [source_node, action2, sink_node2]

                new_set2 = current_set + " " + sink_node2
                new_trans2 = current_trans + [trans2]
                new_choice2 = sink_node2

                work_list.append(new_set2)
                work_list_trans[new_set2] = new_trans2
                work_list_choice[new_set2] = new_choice2

            if check_SCC(SCC, current_choice)[0] != 1:                # while

                SCC_set = check_SCC(SCC, current_choice)[1]

                new_trans = copy.deepcopy(current_trans)
                new_set = copy.deepcopy(current_set)
                for tran in all_trans:
                    if tran[0] in SCC_set and tran[2] in SCC_set:       # in SCC
                        trans = [tran[0], tran[1], tran[2]]
                        new_trans = new_trans + [trans]
                        new_set = new_set + " " + tran[0] + " " + tran[2]

                work_list.append(new_set)
                work_list_trans[new_set] = new_trans
                work_list_choice[new_set] = current_choice
                # delete another branch
                if degree_dir[current_choice][0][1] in SCC_set:
                    degree_dir[current_choice] = [degree_dir[current_choice][1]]
                elif degree_dir[current_choice][1][1] in SCC_set:
                    degree_dir[current_choice] = [degree_dir[current_choice][0]]

    # --------------------------------------------------- store ----------------------------------------- #
    coherent_num = 0
    coherent_file = {}
    non_coherent_file = {}
    non_coherent_num = 0
    copy_file_part = []
    for line in ats.split("\n"):
        if "transitions" in line:
            break
        copy_file_part.append(line)

    trans_list = list(final_result.values())
    for i in range(len(trans_list)):
        segmentation_ats = ""
        for line in copy_file_part:
            segmentation_ats = segmentation_ats + line + "\n"
        segmentation_ats = segmentation_ats + "\ttransitions = {\n"
        for tran in trans_list[i]:
            segmentation_ats = segmentation_ats + "\t\t(" + tran[0] + " " + tran[1] + " " + tran[2] + ")\n"
        segmentation_ats = segmentation_ats + "\t}\n"
        segmentation_ats = segmentation_ats + ");"
        query_begin = time.time()
        if check_gen_program_coherent(segmentation_ats, bpl, save_file=False, print_flag=False):
            if save_file:
                with open("./coherence_" + str(coherent_num) + ".ats", "w") as f:
                    f.write(segmentation_ats)
            coherent_file["./coherence_" + str(coherent_num) + ".ats"] = segmentation_ats
            coherent_num += 1
        else:
            if save_file:
                with open("./noncoherence_" + str(non_coherent_num) + ".ats", "w") as f:
                    f.write(segmentation_ats)
            non_coherent_file["./noncoherence_" + str(non_coherent_num) + ".ats"] = segmentation_ats
            non_coherent_num += 1
        query_end = time.time()
        query_time = query_time + (query_end-query_begin)
    print("-- query time: ", query_time)



    if len(coherent_file) == 0:
        return {}, non_coherent_file
    elif len(non_coherent_file) == 0:
        return coherent_file, {}
    else:
        return coherent_file, non_coherent_file





if __name__ == "__main__":

    boogie_file = "../benchmark/Program/simple_example_ori.bpl"

    # ------------------------- test example -------------------------------------#


    bpl = assert_2_assume(boogie_file)
    ats = boogie_to_automata(bpl, save_file=True, print_flag=False)
    partition(ats, bpl, save_file=True, print_flag=True)

