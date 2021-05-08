#!/usr/bin/env python
#-*- coding:utf-8 -*-

# ------------------------------------------ important to func uodate ----------------------------------------------- #

# for two cases defined in the paper
def function_update(Q, fun_and_vars, left_var, ret_var):
    # Q: current state
    # fun_and_vars: function name and its vars
    # left_var: the assignment statement's var
    # ret_var: variable return by fun

    fun_vars = fun_and_vars[fun_and_vars.find("(")+1:fun_and_vars.find(")")].split(", ")

    if ret_var != "undef" and not (left_var in fun_vars):           # Ensure that the function output is not empty, and left_var is irrevelant to  the function input
        for ret_var_equiv in Q.equivalence[ret_var]:                # the equivalence class of the function output
            if ret_var_equiv != left_var:                           # As long as there is an element different from left_var in the equivalence class, use the new equivalence class of the element as the function output
                Q.Function[fun_and_vars] = ret_var_equiv
                break
            else:
                Q.Function[fun_and_vars] = "undef"
    else:
        Q.Function[fun_and_vars] = "undef"

    return Q


# for three cases defined in the paper
def function_update_complex(Q, other_fun_and_vars, left_var, fun_and_vars):
    # Q: current state
    # other_fun_and_vars: function name and its vars (that to be considered)
    # left_var: the assignment statement's var
    # fun_and_vars: function name and its vars (that to be provided by statement)

    fun_name = fun_and_vars[:fun_and_vars.find("(")]
    fun_var_name = fun_and_vars[fun_and_vars.find("(") + 1:fun_and_vars.find(")")].split(", ")
    other_fun_name = other_fun_and_vars[:other_fun_and_vars.find("(")]
    other_fun_var_name = other_fun_and_vars[other_fun_and_vars.find("(") + 1:other_fun_and_vars.find(")")].split(", ")

    # ---------------h!=f----------------#
    if other_fun_name != fun_name:
        ret_var = Q.Function[other_fun_and_vars]
        Q = function_update(Q, other_fun_and_vars, left_var, ret_var)
    # ---------------h==f----------------#
    else:
        if not (left_var in other_fun_var_name):  # left_var does not appear in the variable of the function
            flag = False  # Determine whether there is a one-to-one correspondence between the two function variables
            for i in range(len(fun_var_name)):
                if fun_var_name[i] in Q.equivalence[other_fun_var_name[i]]:
                    flag = True
                else:
                    flag = False
                    break
            if flag:
                Q.Function[other_fun_and_vars] = left_var
                return Q

        ret_var = Q.Function[other_fun_and_vars]
        function_update(Q, other_fun_and_vars, left_var, ret_var)

    return Q



# --------------------------------------------------------- other ------------------------------------------------------------ #



# --------------------------------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    pass