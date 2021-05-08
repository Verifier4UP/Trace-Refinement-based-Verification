#!/usr/bin/env python
#-*- coding:utf-8 -*-

from Verifier4UP.src.Parser.parsing_bpl import parsing_bpl
from Verifier4UP.src.Coherence.auxiliary import get_while_guard

#
# given an automata file(.ats)， return the corresponding Boogie file(.bpl)
#


def automata2Boogie(bpl, ats, name):


    # Get the string and dir corresponding to boogie_file
    dir = parsing_bpl(bpl, False)
    new_dir = {}
    for item in dir.keys():
        new_dir[dir[item]] = item
    entry_point = get_while_guard(bpl)[0]



    # Get the string and transition corresponding to automata_file
    ats_lst = ats.split("\n")
    # for example: degree_dir = {"q0": [["A", "q1"]], "q1"： [["B", "q2"], ["C", "q3"]], ....}
    flag = False
    degree_dir = {}
    action = []
    for line in ats_lst:
        if flag:
            if "}" in line:
                break
            line = line.strip()[1:-1].split(" ")
            if line[0] in degree_dir.keys():
                degree_dir[line[0]].append([line[1], line[2]])
            else:
                degree_dir[line[0]] = [[line[1], line[2]]]
            action.append(line[1])
        if "transition" in line:
            flag = True


    # Start to construct the corresponding boogie_file
    new_bpl = "type A;\n"
    functions = []
    variables = []
    for alphabet in action:
        statement = new_dir[alphabet]
        if "(" in statement and not("assume" in statement):
            functions.append(statement[statement.find("=") + 2: statement.find("(")])
            variables.append(statement[:statement.find(":") - 1])
            variables.append(statement[statement.find("(") + 1: statement.find(")")])
        elif "assume" in statement:
            variables.append(statement[statement.find("(") + 1: statement.rfind("=") - 2])
            variables.append(statement[statement.rfind("=") + 2: statement.find(")")])
        else:
            variables.append(statement[: statement.find(":") - 1])
            variables.append(statement[statement.find("=") + 2:])
    functions = list(set(functions))
    variables = list(set(variables))

    for fun in functions:
        new_bpl += "function " + fun + "(x: A) returns (A);\n"
    new_bpl += "procedure main(){\n"
    var_str = ""
    for var in variables:
        var_str += (var + ", ")
    new_bpl += ("\tvar " + var_str[0:-2] + ": A;\n\n")

    # Construct the program body
    current_node = "q0"
    already_passed_state = {}
    while_flag = False
    while current_node in degree_dir.keys():
        if len(degree_dir[current_node]) == 1:
            statement = new_dir[degree_dir[current_node][0][0]]
            next_node = degree_dir[current_node][0][1]
            if next_node in already_passed_state.keys():    # the end of while
                new_bpl += ("\t\t" + statement + ";\n\t}\n")
                while_flag = False
                current_node = already_passed_state[next_node]
            else:
                if while_flag:
                    new_bpl += ("\t\t" + statement + ";\n")
                else:
                    new_bpl += ("\t" + statement + ";\n")
                current_node = next_node
        elif len(degree_dir[current_node]) == 2:
            statement1 = new_dir[degree_dir[current_node][0][0]]
            next_node1 = degree_dir[current_node][0][1]
            statement2 = new_dir[degree_dir[current_node][1][0]]
            next_node2 = degree_dir[current_node][1][1]
            # if int(next_node1[1:]) < int(next_node2[1:]):
            if statement2 in entry_point:
                new_bpl += ("\twhile " + statement2[statement2.find("("):] + " {\n")
                already_passed_state[current_node] = next_node1
                current_node = next_node2
            else:
                new_bpl += ("\twhile " + statement1[statement1.find("("):] + " {\n")
                already_passed_state[current_node] = next_node2
                current_node = next_node1
            while_flag = True
    new_bpl += "}"


    with open(name, 'w') as f:
        f.write(new_bpl)



if __name__ == "__main__":

    origin_bpl = "../../program.bpl"
    bpl = ""
    with open(origin_bpl, 'r') as f:
        for line in f:
            bpl = bpl + line

    automata_file = "../../noncoherence_0.ats"
    ats = ""
    with open(automata_file, 'r') as f:
        for line in f:
            ats = ats + line

    name = automata_file[automata_file.rfind(".")] + ".bpl"

    # ------------------------- test example -------------------------------------#

    automata2Boogie(bpl, ats, name)

