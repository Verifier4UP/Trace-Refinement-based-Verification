#!/usr/bin/env python
#-*- coding:utf-8 -*-
import copy



# --------------------------------------------------------- auxiliary func ------------------------------------------------------------ #

# get the info of funs and vars based on the string corresponded to .bpl
def get_fun_var(bpl):

    bpl_lst = bpl.split("\n")

    vars = []               # ["x", "y"]
    funs = [[]]             # [[], ["f"], ["g", "h"], ...], corresponded to 0-ary func，1-ary，2-ary，...
    for line in bpl_lst:
        if "var" in line:
            vars = line[line.find("var")+4:line.find(":")].split(", ")
        if ":=" in line and "(" in line:
            right_vars = line[line.find("(") + 1: line.find(")")].split(", ")
            fun = line[line.find(":=") + 3: line.find("(")]
            for i in range(len(right_vars) + 1):  # check from 0-ary func
                if i >= len(funs):  # there is not i-ary func
                    funs.append([])
                if i == len(right_vars):
                    if not (fun in funs[i]):
                        funs[i].append(fun)
    return vars, funs


# if term is a superterm of var, like f(x,y); x
def IsSuperterm(Function, term, var):

    # direct judgement
    if var in term:
        flag = True
    # indirect judgement
    else:
        flag = False
        candidate = []                  # term
        candidate_vars = []             # term's variable
        previous_candidate_vars_list = []
        # find the superterm of first layer's variable
        for fun in Function.keys():
            if var in fun[fun.find("(")+1: fun.rfind(")")].split(", ") and Function[fun] != "undef":
                candidate.append(fun)
                candidate_vars.append(Function[fun])


        # find superterm layer by layer
        while len(candidate) != 0:
            if term in candidate:
                flag = True
                break
            else:
                if set(candidate_vars) in previous_candidate_vars_list:       # Prevent falling into an endless loop
                    break
                else:
                    previous_candidate_vars_list.append(set(candidate_vars))
                previous_candidate_vars = list(set(copy.deepcopy(candidate_vars)))  # Deduplication
                candidate = []          # term
                candidate_vars = []     # term's variable
                for candidate_var in previous_candidate_vars:
                    for fun in Function.keys():
                        if candidate_var in fun[fun.find("(")+1: fun.rfind(")")].split(", "):
                            candidate.append(fun)
                            if Function[fun] != "undef":
                                candidate_vars.append(Function[fun])
    return flag




# Detect whether a statement brings memorizing threat
# (1) This statement may cause an item in the previous state to disappear
# (2) View all equivalent items of the item
# (3) See if these equivalent items are mapped to undef in the new state
def item_info_loss(Q_current, Q_previous, statement):


    change_var = statement[:statement.find(":")-1]

    # --------------------------------------------------------------------------- #
    # As long as the saved item has no variable saved now, it is los
    for fun in Q_previous.Function.keys():
        if Q_previous.Function[fun] == change_var and Q_current.Function[fun] == "undef":
            return True, change_var
    return False, ""


# Get loop guard information
def get_while_guard(bpl):

    bpl_lst = bpl.split("\n")

    entry_point = []
    exit_point = []
    for line in bpl_lst:
        if "while" in line:
            left_var = line[line.find("(")+1:line.rfind("=")-2]
            right_var = line[line.rfind("=")+2:line.find(")")]
            if "!=" in line:
                entry_point.append("assume(" + left_var + " != " + right_var + ")")
                exit_point.append("assume(" + left_var + " == " + right_var + ")")
            else:
                entry_point.append("assume(" + left_var + " == " + right_var + ")")
                exit_point.append("assume(" + left_var + " != " + right_var + ")")

    return entry_point, exit_point


# --------------------------------------------------------- others ------------------------------------------------------------ #
# Generate Cartesian product of two lists
def list_product(list1, list2):
    return [str(x) + " " + str(y) for x in list1 for y in list2]





# --------------------------------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    pass

    # Function = {"f(x)": "y", "g(x)": "z", "h(z)": "w"}
    # term = "h(z)"
    # var = "x"
    # print(IsSuperterm(Function, term, var))