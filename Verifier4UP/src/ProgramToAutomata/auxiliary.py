#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
import copy
from Verifier4UP.src.Parser.parsing_bpl import parsing_bpl

# ------------------------------Convert the automaton obtained by ULTIMATE into a standard format-----------------#
def automata_to_automata(bpl, print_flag):


    # --------------------Parse the automata file obtained by ULTIMATE to get all the migrations-------------------#
    flag = False
    with open("program_tmp.ats", 'r') as f:
        for line in f:
            if "transitions" in line:
                flag = True
                transitions = []
            else:
                if flag:
                    transitions.append(line[line.find("(")+1: line.rfind(")")])
                else:
                    pass
        transitions = transitions[0:-2]


    # -------------------------------Adjust the transition block----------------------------#
    if print_flag:
        print("original transition:")
        for item in transitions:
            print(item)
        print("\n")
    To_be_removed = []
    To_be_added = []
    new_end_idx_dir = {}        # When split the block, it's used to mark the newly generated state
    for trans in transitions:
        if "BeginParallelComposition" in trans:
            [tran_lst, new_end_idx_dir] = block_translator(trans, new_end_idx_dir)
            To_be_added = To_be_added + tran_lst
            To_be_removed.append(trans)
    for item in To_be_removed:
        transitions.remove(item)
    for item in To_be_added:
        transitions.append(item)


    # -------------------------------the info between statememt and alphabet--------------------------#

    # Maintain consistency with the order of statements in the bpl file
    alphabet_dir = parsing_bpl(bpl, print_flag=False)
    if print_flag:
        print("original alphabet_dir:")
        print_dir = sorted(alphabet_dir.items(), key=lambda x: x[1], reverse=False)
        for item in print_dir:
            print(item[1], ":", item[0])
        print("\n")
    origin_keys = copy.deepcopy(list(alphabet_dir.keys()))
    for item in origin_keys:
        if "assume" in item and "==" in item:
            left_var = item[item.find("(") + 1:item.rfind("=") - 2]
            right_var = item[item.rfind("=") + 2:item.rfind(")")]
            item1 = "assume " + left_var + " == " + right_var
            item2 = "assume !(" + left_var + " != " + right_var + ")"
            item3 = "assume （" + left_var + " == " + right_var + ")"
            value = alphabet_dir[item]
            alphabet_dir[item1] = value
            alphabet_dir[item2] = value
            alphabet_dir[item3] = value
        elif "assume" in item and "!=" in item:
            left_var = item[item.find("(") + 1:item.rfind("=") - 2]
            right_var = item[item.rfind("=") + 2:item.rfind(")")]
            item1 = "assume " + left_var + " != " + right_var
            item2 = "assume !(" + left_var + " == " + right_var + ")"
            item3 = "assume （" + left_var + " != " + right_var + ")"
            value = alphabet_dir[item]
            alphabet_dir[item1] = value
            alphabet_dir[item2] = value
            alphabet_dir[item3] = value

    if print_flag:
        print("new alphabet_dir:")
        print_dir = sorted(alphabet_dir.items(), key=lambda x: x[1], reverse=False)
        for item in print_dir:
            print(item[1], ":", item[0])
        print("\n")



    # -----------------------------------Transform the transition information------------------------------#
    trans_list = []                 # the final transition list
    states_dir = {"mainENTRY": 0}   # Correspondence between the state of the original automaton and the state of the new automaton
    state_idx = 0                   # Current latest state

    # Adjust the order of transition to facilitate the statistics of the state sequence number
    # (the state corresponding to each start must have already appeared)
    mainENTRY = []
    mainEXIT = []
    mainend = []
    existing_exit = [] # Collect the nodes that have appeared, to facilitate the sorting later
    for trans in transitions:
        if trans[1:-1].split('" "')[0] == "mainENTRY":
            mainENTRY.append(trans)
            existing_exit.append(trans[1:-1].split('" "')[2])
        elif trans[1:-1].split('" "')[2] == "mainEXIT":
            mainEXIT.append(trans)
        elif "--" in trans[1:-1].split('" "')[0]:
            mainend.append(trans)
    for item in mainENTRY:
        transitions.remove(item)
    for item in mainEXIT:
        transitions.remove(item)
    for item in mainend:
        transitions.remove(item)
    new_transitions = []
    transitions.sort()
    while transitions != []:
        for trans in transitions:
            if trans[1:-1].split('" "')[0] in existing_exit:
                new_transitions.append(trans)
                existing_exit.append(trans[1:-1].split('" "')[2])
                transitions.remove(trans)
                break
    transitions = mainENTRY + new_transitions + mainend + mainEXIT
    if print_flag:
        print("new transition:")
        for item in transitions:
            print(item)
        print("\n")

    # After the sequence conversion, the state transition begins
    for trans in transitions:
        trans = trans[1:-1].split('" "')
        start = trans[0]
        action = trans[1][0:-1].split(";")
        end = trans[2]
        if end != "mainErr0ASSERT_VIOLATIONASSERT":
            if len(action) != 1:
                # the first action
                trans_list.append("(q" + str(states_dir[start]) + " " + alphabet_dir[action[0]] + " q" + str(state_idx + 1) + ")")
                state_idx += 1

                # the middle action
                for act in action[1:-1]:
                    if act != "assume true":
                        trans_list.append("(q" + str(state_idx) + " " + alphabet_dir[act] + " q" + str(state_idx + 1) + ")")
                        state_idx += 1

                # the last action
                if end in states_dir.keys():
                    trans_list.append("(q" + str(state_idx) + " " + alphabet_dir[action[-1]] + " q" + states_dir[end] + ")")
                else:
                    if action[-1] != "assume true":
                        trans_list.append("(q" + str(state_idx) + " " + alphabet_dir[action[-1]] + " q" + str(state_idx + 1) + ")")
                        state_idx += 1
                    states_dir[end] = str(state_idx)

            else:
                # the last action
                if end in states_dir.keys():
                    trans_list.append("(q" + str(states_dir[start]) + " " + alphabet_dir[action[-1]] + " q" + states_dir[end] + ")")
                else:
                    trans_list.append("(q" + str(states_dir[start]) + " " + alphabet_dir[action[-1]] + " q" + str(state_idx + 1) + ")")
                    state_idx += 1
                    states_dir[end] = str(state_idx)


    # -----------------------------------rewrite automata------------------------------#
    new_ats = ""

    new_ats = new_ats + "FiniteAutomaton FSM = (\n"

    # alphabet
    alphabet_line = "\talphabet = {"
    alphabet_list = list(set(list(alphabet_dir.values())))
    alphabet_list.sort()
    for item in alphabet_list:
        alphabet_line = alphabet_line + item + " "
    alphabet_line = alphabet_line[0:-1] + "},\n"
    new_ats = new_ats + alphabet_line

    # states
    states_line = ""
    for i in range(state_idx + 1):
        states_line = states_line + "q" + str(i) + " "
    new_ats = new_ats + "\tstates = {" + states_line[0:-1] + "},\n"
    new_ats = new_ats + "\tinitialStates = {q0},\n"
    new_ats = new_ats + "\tfinalStates = {q" + str(state_idx) + "},\n"

    # transitions
    new_ats = new_ats + "\ttransitions = {\n"
    for item in trans_list:
        if states_dir["mainEXIT"] != state_idx:
            charmap = {"q"+str(states_dir["mainEXIT"]): "q"+str(state_idx),
                       "q"+str(state_idx): "q"+str(states_dir["mainEXIT"])}
            item = re.sub(r'"q"+str(states_dir["mainEXIT"])|"q"+str(state_idx)', lambda x:charmap[x.group(0)], item)
        new_ats = new_ats + "\t\t" + item + "\n"
    new_ats = new_ats + "\t}\n"
    new_ats = new_ats + ");"

    return new_ats



# -----------------------------------Convert transition with blocks-----------------------------#
def block_translator(tran, new_end_idx_dir):

    work_lst = [tran]
    tran_lst = []

    while work_lst != []:
        block_tran = work_lst.pop()
        # Cut off the sequence module before and after
        # print(block_tran)
        [tran_lst, new_end_idx_dir, start, mid_block, end] = pre_split(block_tran, tran_lst, new_end_idx_dir)
        # heck whether there exists parallel block
        # print(mid_block)
        [check_flag, check_list, new_end_idx_dir] = check_parallel(start, mid_block, end, new_end_idx_dir)
        # print(check_flag)
        if check_flag:
            for tran in check_list:
                work_lst.append(tran)
        else:
            current_tran = '"' + start + '" "' + mid_block + '" "' + end + '"'
            [work_lst, tran_lst, new_end_idx_dir] = single_block_translator(current_tran, work_lst, tran_lst, new_end_idx_dir)

    return tran_lst, new_end_idx_dir




# Strip out the sequence statements before and after
def pre_split(tran, tran_lst, new_end_idx_dir):

    # -------------------- first tackle: start, action, end------------------------ #
    tran = tran[1: -1].split('" "')
    start = tran[0]
    action = tran[1]
    # Each action of the initial transition statement must end with;
    if action[-1] != ";": action = action + ";"
    # All EndParallelComposition must end with;
    index = 0
    result = re.search(r'EndParallelComposition', action)
    while result != None:
        index = result.span()[1] + index
        if action[index] != ";":
            action = action[:index] + ";" + action[index:]
            index += 1
        result = re.search('EndParallelComposition', action[index:])
    end = tran[2]


    pre_block = action[:action.find("BeginParallelComposition")]
    mid_block = action[action.find("BeginParallelComposition"): action.rfind("EndParallelComposition;") + 23]
    post_block = action[action.rfind("EndParallelComposition;") + 23:]



    # --------------------------- Add pre-transtion and post-transition ------------------------------- #
    start_ori = copy.deepcopy(start)
    end_ori = copy.deepcopy(end)
    if not (start_ori in new_end_idx_dir.keys()):
        new_end_idx_dir[start_ori] = 0
    tmp_start_idx = new_end_idx_dir[start]
    if not (end_ori in new_end_idx_dir.keys()):
        new_end_idx_dir[end_ori] = 0
    tmp_end_idx = new_end_idx_dir[end]
    if pre_block != "":
        tran_lst.append('"' + start + '" "' + pre_block + '" "' + start + "_" + str(tmp_start_idx) + '"')
        start = start + "_" + str(tmp_start_idx)
        new_end_idx_dir[start_ori] += 1
    if post_block != "":
        tran_lst.append('"' + end + "--" + str(tmp_end_idx) + '" "' + post_block + '" "' + end + '"')
        end = end + "--" + str(tmp_end_idx)
        new_end_idx_dir[end_ori] += 1

    return tran_lst, new_end_idx_dir, start, mid_block, end

# Check if there is a block with parallel structure
def check_parallel(start, tran, end, new_end_idx_dir):

    check_list = [] # given the list of (start, tran, end)
    check_flag = False

    tran_lst = re.split(r'(BeginParallelComposition|EndParallelComposition;)', tran)
    while "" in tran_lst:
        tran_lst.remove("")
    composition_pair_flag = 0
    repeat_pair_record = [0]     # Record the update of the match
    initial = 0
    for i in range(len(tran_lst)):
        statement = tran_lst[i]
        if statement == "BeginParallelComposition":
            composition_pair_flag += 1
        elif statement == "EndParallelComposition;":
            composition_pair_flag -= 1
            # It has appeared twice, and there are no more blocks in between, it can be explained that it is a parallel block of the same level
            if composition_pair_flag == 0 and repeat_pair_record.count(composition_pair_flag) == 2:
                check_flag = True
        else:
            continue
        repeat_pair_record.append(composition_pair_flag)


        if composition_pair_flag == 0:
            transition = ""
            for item in tran_lst[initial: i + 1]:
                transition = transition + item
            if i == len(tran_lst)-1:
                check_list.append('"' + start + '" "' + transition + '" "' + end + '"')
            else:
                if not (start in new_end_idx_dir.keys()):
                    new_end_idx_dir[start] = 0
                tmp_start_idx = new_end_idx_dir[start]
                check_list.append('"' + start + '" "' + transition + '" "' + start + "_" + str(tmp_start_idx) + '"')  # 平行block
                new_end_idx_dir[start] += 1
                start = start + "_" + str(tmp_start_idx)
            initial = i + 1


    return check_flag, check_list, new_end_idx_dir

# Convert non-parallel blocks
def single_block_translator(tran, work_lst, tran_lst, new_end_idx_dir):

    # -------------------- first tackle: start, action, end------------------------ #
    tran = tran[1: -1].split('" "')
    start = tran[0]
    action = tran[1]
    end = tran[2]

    # get the key identification of each block
    key_pattern = re.compile(r'{ParallelCodeBlock0: assume (.*?);')
    key_assume = re.findall(key_pattern, action)[0]
    if "!(" in key_assume:
        key_assume = key_assume[key_assume.find("(")+1:key_assume.find(")")]
        key_assume0 = "!(" + key_assume + ")"
        key_assume1 = key_assume
        pattern0 = re.compile(r'Block0: assume !\(' + key_assume + '\)(.*?)ParallelCodeBlock1: assume ' + key_assume)
        pattern1 = re.compile(r'Block1: assume ' + key_assume + '(.*)}End')
    else:
        key_assume0 = key_assume
        key_assume1 = "!(" + key_assume + ")"
        pattern0 = re.compile(r'Block0: assume ' + key_assume + '(.*?)ParallelCodeBlock1: assume !\(' + key_assume + '\)')
        pattern1 = re.compile(r'Block1: assume !\(' + key_assume + '\)(.*)}End')


    block0 = re.findall(pattern0, action)[0]
    block1 = re.findall(pattern1, action)[0]
    if block0[-1] != ";": block0 = block0 + ";"  # Ensure that every action ends with;
    if block1[-1] != ";": block1 = block1 + ";"


    # middle splition
    if "Block" in block0:
        work_lst.append('"' + start + '" "assume ' + key_assume0 + block0 + '" "' + end + '"')
    else:
        if tran_lst == []:
            tran_lst = ['"' + start + '" "assume ' + key_assume0 + block0 + '" "' + end + '"']
        else:
            tran_lst.append('"' + start + '" "assume ' + key_assume0 + block0 + '" "' + end + '"')


    if "Block" in block1:
        work_lst.append('"' + start + '" "assume ' + key_assume1 + block1 + '" "' + end + '"')
    else:
        if tran_lst == []:
            tran_lst = ['"' + start + '" "assume ' + key_assume1 + block1 + '" "' + end + '"']
        else:
            tran_lst.append('"' + start + '" "assume ' + key_assume1 + block1 + '" "' + end + '"')

    return work_lst, tran_lst, new_end_idx_dir




if __name__ == "__main__":
    pass