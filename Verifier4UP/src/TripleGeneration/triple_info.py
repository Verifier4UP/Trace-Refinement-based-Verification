#!/usr/bin/env python
#-*- coding:utf-8 -*-

import copy
import itertools


class triple:

    # --------------------------------- Basic triple-info ------------------------------------------------- #
    def __init__(self, vars, funs, idx):
        self.vars = vars            # vars
        self.funs = funs            # funcs
        self.index = idx            # index
        self.equivalence = {}       # equivalence (directory) {"x":["x","y"], "z":["z"], ...}
        self.state = "undef"         # accept or reject

        # 重要关系
        self.Equality = []          # Equality   (list)         [("x", "x"), ("x", "y"), ...]
        self.Disequality = []       # Disequality (list)        [("[x]", "[y]"), ...]
        self.Function = {}          # Function   (directory)    {"f(x)":"y", "g(y)":"undef", ...}
        for var in vars:
            self.Equality.append((var, var))
            self.equivalence[var] = [var]
        for i in range(1, len(funs)):
            for fun in funs[i]:
                possible_vars = [', '.join(x) for x in itertools.product(*[vars] * i)]  # Generate possible combinations of function and variables
                for each_possible_vars in possible_vars:
                    self.Function[fun + "(" + each_possible_vars + ")"] = "undef"



    # -------------------------------------update--------------------------------------------------- #

    def update(self):
        # Update the equivalence class first
        # and then determine whether certain functions should be merged based on the new equivalence class relationship
        self.update_equivalence()
        self.update_congruence()
        # self.update_earlyassume_equivalence()
        self.accept_or_reject()


    # update equivalence after triple info fixed
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
                            # update Equality
                            # example:
                            # current:  x1=f(x0), x2=f(x1), y1=f(y0), y2=f(y1) while x0==y0
                            # after:            assume(x0 == y0)
                            # then:     Equality: {x0: [x0, y0]}
                            # fix:      Equality: {x0: [x0, y0], x1: [x1, y1], x2: [x2,y2]}
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


    # state evalutaion
    def accept_or_reject(self):
        for disequal_pair in self.Disequality:
            left = disequal_pair[0][1:-1]
            right = disequal_pair[1][1:-1]
            for item in self.equivalence[left]:
                if item in self.equivalence[right]:
                    self.state = "reject"
                    return "reject"
        self.state = "accept"
        return "accept"


    # -------------------------------------other--------------------------------------------------- #

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
        print("\nstate: ", self.state)
        print("==============================\n")



if __name__ == "__main__":
    pass