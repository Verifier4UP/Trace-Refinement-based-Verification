#!/usr/bin/env python
#-*- coding:utf-8 -*-

import copy
import itertools
from functools import reduce
from Verifier4UP.src.Coherence.auxiliary import IsSuperterm, list_product


class quad_info:

    # --------------------------------- Basic quadruple-info ------------------------------------------------- #
    def __init__(self, vars, funs, idx):

        self.vars = vars            # vars
        self.funs = funs            # funs
        self.index = idx            # index
        self.equivalence = {}       # equivalence (directory) {"x":["x","y"], "z":["z"], ...}

        self.Equality = []          # Equality      (list)                              [("x", "x"), ("x", "y"), ...]
        self.Disequality = []       # Disequality   (list)                              [("[x]", "[y]"), ...]
        self.Function = {}          # Function      (directory)                         {"f(x)":"y", "g(y)":"undef", ...}
        self.Item = []              # the term has been calculated so far   (list)      ["f(x)", "g(x,y)", ...]
        for var in vars:
            self.Equality.append((var, var))
            self.equivalence[var] = [var]
        for i in range(1, len(funs)):
            for fun in funs[i]:
                possible_vars = [', '.join(x) for x in itertools.product(*[vars] * i)]  # Generate possible combinations of function and variables
                for each_possible_vars in possible_vars:
                    self.Function[fun + "(" + each_possible_vars + ")"] = "undef"


    # -------------------------------------update--------------------------------------------------- #

    def update(self, stat):
        if ":=" in stat and "(" in stat:  # x := f(y)
            # ------------------ for item， update twice--------------------#
            ## The first time should be completed before updating to the latest equivalence class
            # mainly to deal with the situation of x=f(x)
            # because the old equivalence class of x should be added to the item at this time
            self.update_item(stat, "before")
            # update equivalence
            self.update_equivalence()
            self.update_congruence()
            ## The second time is to be completed after updating to the latest equivalence class
            # because after x is updated, some of its corresponding new equivalence classes are in item
            # then x should also be replaced
            self.update_item(stat, "after")
        elif ":=" in stat:                 # x:=y
            self.update_equivalence()
            self.update_congruence()
            ## The second time is to be completed after updating to the latest equivalence class
            # because after x is updated, some of its corresponding new equivalence classes are in item
            # then x should also be replaced
            self.update_item(stat, "after")
        else:
            self.update_equivalence()
            self.update_congruence()




    # update equivalence after quad info fixed
    def update_equivalence(self):
        # initialization
        for var in self.vars:
            self.equivalence[var] = []
        # update
        for var in self.vars:   # "x"
            for var_tuple in self.Equality:
                if var in var_tuple:
                    if not(var_tuple[0] in self.equivalence[var]):      # ("y", "x")
                        self.equivalence[var].append(var_tuple[0])
                    elif not(var_tuple[1] in self.equivalence[var]):    # ("x", "y")
                        self.equivalence[var].append(var_tuple[1])

    # make fun's congruence consistent:
    def update_congruence(self):
        old_Equality = []
        old_Function = []
        while self.Equality != old_Equality and self.Function != old_Function:  # exit from fix-point
            old_Equality = self.Equality
            old_Function = self.Function

            for fun_and_vars in self.Function:
                fun_name = fun_and_vars[:fun_and_vars.find("(")]
                fun_var_name = fun_and_vars[fun_and_vars.find("(") + 1:fun_and_vars.find(")")].split(", ")
                ret_var = self.Function[fun_and_vars]
                for other_fun_and_vars in self.Function:
                    other_fun_name = other_fun_and_vars[:other_fun_and_vars.find("(")]
                    other_fun_var_name = other_fun_and_vars[other_fun_and_vars.find("(") + 1:other_fun_and_vars.find(")")].split(", ")
                    other_ret_var = self.Function[other_fun_and_vars]
                    if fun_name == other_fun_name and fun_and_vars != other_fun_and_vars:  # Only consider when two function is different
                        # Compare the parameters one by one
                        congruence_flag = False
                        for i in range(len(fun_var_name)):
                            if fun_var_name[i] in self.equivalence[other_fun_var_name[i]]:
                                congruence_flag = True
                            else:
                                congruence_flag = False
                                break
                        if congruence_flag == True:     # Two functions are equal in the sense of equivalence class
                            # update Function
                            # example:
                            # current:  f(y)=g    /\   f(g)=x
                            # after:          y=f(y)
                            # then:     f(y)=undef /\ f(g)=x   meanwhile g=y
                            # fix:      f(y)=x    /\ f(g)=x
                            if ret_var == "undef" and other_ret_var != "undef":
                                self.Function[fun_and_vars] = other_ret_var
                            elif other_ret_var == "undef" and ret_var != "undef":
                                self.Function[other_fun_and_vars] = ret_var
                            # update Equality
                            # example:
                            # current:  x1=f(x0), x2=f(x1), y1=f(y0), y2=f(y1) while x0==y0
                            # after:            assume(x0 == y0)
                            # then:     Equality: {x0: [x0, y0]}
                            # fix:      Equality: {x0: [x0, y0], x1: [x1, y1], x2: [x2,y2]}
                            elif ret_var != "undef" and other_ret_var != "undef":
                                if not (ret_var in self.equivalence[other_ret_var]):  # the missing equivalence classes
                                    for equivalence_var_left in self.equivalence[ret_var]:
                                        for equivalence_var_right in self.equivalence[other_ret_var]:
                                            self.Equality.append((equivalence_var_left, equivalence_var_right))
                                            self.Equality.append((equivalence_var_right, equivalence_var_left))
                                            self.Equality = list(set(self.Equality))  # Deduplication
                                        self.update_equivalence()   # Update equivalence based on Equality

    def update_item(self, stat, flag):
        left_var = stat[:stat.find(":=") - 1]
        right_fun = stat[stat.find(":=") + 3:]
        fun_name = right_fun[:right_fun.find("(")]

        if flag == "before":
            # Because the function is determined to be equal to term x, the equivalent terms of the function term must be added
            # -----------------Add------------------#
            equivalence_fun_vars = []   # Store the equivalent classes corresponding to the function variables
            fun_vars = right_fun[right_fun.find("(") + 1: right_fun.find(")")].split(", ")
            for var in fun_vars:
                equivalence_fun_vars.append(self.equivalence[var])
            possible_match = reduce(list_product, equivalence_fun_vars)
            for each_match in possible_match:
                if not(fun_name + "(" + each_match + ")" in self.Item):
                    each_match = each_match.replace(" ", ", ")
                    self.Item.append(fun_name + "(" + each_match + ")")

            # Items related to x must be deleted because x has changed
            # ---------------Remove-----------------#
            To_be_remove = []
            for item in self.Item:
                if left_var in item[item.find("(")+1: item.rfind(")")].split(", "):
                    To_be_remove.append(item)
            for item in To_be_remove:
                self.Item.remove(item)
        else:
            # Items related to x must be deleted because x has changed. (Here x := y does not take the before route, so it needs to be deleted separately)
            # ---------------Remove-----------------#
            To_be_remove = []
            for item in self.Item:
                if left_var in item[item.find("(") + 1: item.rfind(")")].split(", "):
                    To_be_remove.append(item)
            for item in To_be_remove:
                self.Item.remove(item)

            # ------------------Add-----------------#
            To_be_add = []
            for item in self.Item:
                fun_name = item[:item.find("(")]
                fun_vars = item[item.find("(") + 1: item.find(")")].split(", ")
                # Find the positions of all equivalence classes
                label_idx = []
                for i in range(len(fun_vars)):
                    var = fun_vars[i]
                    if var in self.equivalence[left_var]:
                        label_idx.append(i)
                # Permutations
                if len(label_idx) != 0:
                    if len(label_idx) == 1:   # Only one position need to be replaced
                        new_item = fun_name + "(" + left_var + ")"
                        To_be_add.append(new_item)
                    else:                     # multiple positions need to be replaced，then permutations
                        zero_one_list = [["0", "1"]]*len(label_idx)
                        possible_match = reduce(list_product, zero_one_list)
                        for each_match in possible_match:
                            new_fun_vars = copy.deepcopy(fun_vars)
                            for j in range(len(label_idx)):
                                if each_match[2*j] == "1":  # Replace the position of the equivalence class with left_var
                                    new_fun_vars[label_idx[j]] = left_var
                            new_item = ""
                            for var in new_fun_vars:
                                new_item = new_item + var + ", "
                            new_item = fun_name + "(" + new_item[:-2] + ")"
                            To_be_add.append(new_item)
            for new_item in To_be_add:
                if not (new_item in self.Item):
                    self.Item.append(new_item)



    # -------------------------------------other--------------------------------------------------- #

    # Check whether the next statement constitutes a coherent threat to the previous state
    def check_coherent(self, next_statement):
        coherent_flag = True
        # check early assume
        if "assume" in next_statement:
            statement_type = "earlyassume"
            left_var = next_statement[next_statement.find("(") + 1: next_statement.find("==") - 1]
            right_var = next_statement[next_statement.find("==") + 3: next_statement.find(")")]
            for fun in self.Function.keys():
                if IsSuperterm(self.Function, fun, left_var) or IsSuperterm(self.Function, fun, right_var):
                    if self.Function[fun] == "undef" and fun in self.Item:
                        coherent_flag = False
                        break
                    else:
                        coherent_flag = True

        # check memorizing
        else:
            statement_type = "memorizing"
            fun_vars = next_statement[next_statement.find(":=") + 3:]
            if self.Function[fun_vars] == "undef" and fun_vars in self.Item:     # Found that the current item to be calculated has been discarded in the previous state
                coherent_flag = False
            else:
                coherent_flag = True

        return coherent_flag, statement_type



    # print info
    def show(self):
        print("/----------------\\")
        print("| State_index: ", self.index, "|")
        print("\\----------------/")
        print_equivalence = sorted(self.equivalence.items(), key=lambda x: x[0], reverse=False)
        print("equivalence: ", print_equivalence, "\n")
        print_Equality = copy.deepcopy(self.Equality)
        print_Equality.sort()
        print("+ Equality: ", print_Equality)
        print_Disequality = copy.deepcopy(self.Disequality)
        print_Disequality.sort()
        print("+ Disequality: ", print_Disequality)
        print_Function = sorted(self.Function.items(), key=lambda x: x[0], reverse=False)
        print("+ Function: ", print_Function)
        print_Item = copy.deepcopy(self.Item)
        print_Item.sort()
        print("+ Item: ", print_Item)
        print("==============================\n\n\n")



if __name__ == "__main__":
    pass