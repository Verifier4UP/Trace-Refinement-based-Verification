#!/usr/bin/env python
#-*- coding:utf-8 -*-
import copy
from Verifier4UP.src.TripleGeneration.auxiliary import function_update, function_update_complex


# x := y
def rule1(stat, Q_next):

    left_var = stat[:stat.find(":=") - 1]
    right_var = stat[stat.find(":=") + 3:]

    #-------------for Equality----------------#
    # remove
    To_be_remove = []
    for var_tuple in Q_next.Equality:
        if left_var in var_tuple:
            To_be_remove.append(var_tuple)
    for var_tuple in To_be_remove:
        Q_next.Equality.remove(var_tuple)

    # add
    for equivalence_var in Q_next.equivalence[right_var]:
        Q_next.Equality.append((left_var, equivalence_var))
        Q_next.Equality.append((equivalence_var, left_var))
    Q_next.Equality.append((left_var, left_var))
    Q_next.Equality = list(set(Q_next.Equality))    # Deduplication

    # ------------for DisEquality-------------#
    To_be_remove = []
    To_be_add = []
    for equiv_tuple in Q_next.Disequality:
        if "[" + left_var + "]" in equiv_tuple:
            To_be_remove.append(equiv_tuple)
            for equiv_var in Q_next.equivalence[left_var]:  # The inequality of equivalence classes is still there
                if equiv_var != left_var:
                    To_be_add.append(("["+equiv_var+"]", equiv_tuple[1]))
                    break
    for equiv_tuple in To_be_remove:
        Q_next.Disequality.remove(equiv_tuple)
    for equiv_tuple in To_be_add:
        Q_next.Disequality.append(equiv_tuple)

    # ------------for Function----------------#
    for fun_and_vars in Q_next.Function.keys():
        ret_var = Q_next.Function[fun_and_vars]
        Q_next = function_update(Q_next, fun_and_vars, left_var, ret_var)

    return Q_next



# x := f(y)
def rule2(stat, Q_next):

    left_var = stat[:stat.find(":=") - 1]
    right_fun = stat[stat.find(":=") + 3:]

    # ---------------------------------------function is defined---------------------------------------#
    if Q_next.Function[right_fun] != "undef":
        ret_var = Q_next.Function[right_fun]

        if not (left_var in Q_next.equivalence[ret_var]):   # Only consider the case where left_var does not belong to the output equivalence class

            # -------------for Equality----------------#
            # remove
            To_be_remove = []
            for var_tuple in Q_next.Equality:
                if left_var in var_tuple:
                    To_be_remove.append(var_tuple)
            for var_tuple in To_be_remove:
                Q_next.Equality.remove(var_tuple)

            # add
            for equivalence_var in Q_next.equivalence[ret_var]:
                Q_next.Equality.append((left_var, equivalence_var))
                Q_next.Equality.append((equivalence_var, left_var))
            Q_next.Equality.append((left_var, left_var))
            Q_next.Equality = list(set(Q_next.Equality))    # Deduplication

            # ------------for DisEquality-------------#
            To_be_remove = []
            To_be_add = []
            for equiv_tuple in Q_next.Disequality:
                if "[" + left_var + "]" in equiv_tuple:
                    To_be_remove.append(equiv_tuple)
                    for equiv_var in Q_next.equivalence[left_var]:  # The inequality of equivalence classes is still there
                        if equiv_var != left_var:
                            if "[" + left_var + "]" == equiv_tuple[0]:
                                To_be_add.append(("[" + equiv_var + "]", equiv_tuple[1]))
                            else:
                                To_be_add.append((equiv_tuple[0], "[" + equiv_var + "]"))
                            break
            for equiv_tuple in To_be_remove:
                Q_next.Disequality.remove(equiv_tuple)
            for equiv_tuple in To_be_add:
                Q_next.Disequality.append(equiv_tuple)
            Q_next.Disequality = list(set(Q_next.Disequality))

            # ------------for Function----------------#
            for fun_and_vars in Q_next.Function.keys():
                ret_var = Q_next.Function[fun_and_vars]
                Q_next = function_update(Q_next, fun_and_vars, left_var, ret_var)



    # ---------------------------------------function is undefined---------------------------------------#
    else:
        # -------------for Equality----------------#
        # remove
        To_be_remove = []
        for var_tuple in Q_next.Equality:
            if left_var in var_tuple:
                To_be_remove.append(var_tuple)
        for var_tuple in To_be_remove:
            Q_next.Equality.remove(var_tuple)

        # add
        Q_next.Equality.append((left_var, left_var))
        Q_next.Equality = list(set(Q_next.Equality))    # Deduplication

        # ------------for DisEquality-------------#
        To_be_remove = []
        To_be_add = []
        for equiv_tuple in Q_next.Disequality:
            if "[" + left_var + "]" in equiv_tuple:
                To_be_remove.append(equiv_tuple)
                for equiv_var in Q_next.equivalence[left_var]:  # The inequality of equivalence classes is still there
                    if equiv_var != left_var:
                        if "[" + left_var + "]" == equiv_tuple[0]:
                            To_be_add.append(("[" + equiv_var + "]", equiv_tuple[1]))
                        else:
                            To_be_add.append((equiv_tuple[0], "[" + equiv_var + "]"))
                        break
        for equiv_tuple in To_be_remove:
            Q_next.Disequality.remove(equiv_tuple)
        for equiv_tuple in To_be_add:
            Q_next.Disequality.append(equiv_tuple)
        Q_next.Disequality = list(set(Q_next.Disequality))

        # ------------for Function----------------#
        for fun_and_vars in Q_next.Function.keys():
            Q_next = function_update_complex(Q_next, fun_and_vars, left_var, right_fun)

    return Q_next



# assume(x == y)
def rule3(stat, Q_next):
    left_var = stat[stat.find("(") + 1: stat.find("==") - 1]
    right_var = stat[stat.find("==") + 3: stat.find(")")]

    # -------------for Equality----------------#
    # add
    for equivalence_var_left in Q_next.equivalence[left_var]:
        for equivalence_var_right in Q_next.equivalence[right_var]:
            Q_next.Equality.append((equivalence_var_left, equivalence_var_right))
            Q_next.Equality.append((equivalence_var_right, equivalence_var_left))
    Q_next.Equality = list(set(Q_next.Equality))    # Deduplication

    # ------------for DisEquality-------------#


    # ------------for Function----------------#


    return Q_next


# assume(x != y)
def rule4(stat, Q_next):
    left_var = stat[stat.find("(") + 1: stat.find("!=") - 1]
    right_var = stat[stat.find("!=") + 3: stat.find(")")]

    # -------------for Equality----------------#


    # ------------for DisEquality-------------#
    # add
    if ("[" + left_var + "]", "[" + right_var + "]") in Q_next.Disequality:
        pass
    else:
        Q_next.Disequality.append(("[" + left_var + "]", "[" + right_var + "]"))


    # ------------for Function----------------#

    return Q_next

if __name__ == "__main__":
    pass