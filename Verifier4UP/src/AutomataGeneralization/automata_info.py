#!/usr/bin/env python
#-*- coding:utf-8 -*-
import copy
import turtle
import numpy as np


class automata:

    # --------------------------------- Basic Info ------------------------------------------------- #
    def __init__(self, alphabet=[], states=[0], initial_state=0, accepted_states=[], transition=[]):
        self.alphabet = alphabet                        # action set
        self.states = states                            # state set
        self.initial_state = initial_state              # initial state
        self.accepted_states = accepted_states          # accepted states
        self.transition = transition                    # transitions

    def add_transition(self, trans):  # trans = [from_node, action, to_node]
        # update alphabet
        if not (trans[1] in self.alphabet):
            self.alphabet.append(trans[1])
        # update states
        if not (trans[0] in self.states):
            self.states.append(trans[0])
        if not (trans[2] in self.states):
            self.states.append(trans[2])
        # update transition
        if not (trans in self.transition):
            self.transition.append(trans)


    # --------------------------------- combination ------------------------------------------------- #
    # currently we consider the combination of two adjacent states, need to update the following infos:
    # self, state_map, program_sequence, loop_flag
    def combine_state(self, state1, state2, state_map, program_sequence, loop_flag):

        # ------------------------- modify states -------------------------------- #
        ## self
        self.states.remove(max(self.states))    # remove the last state
        ## state_map
        state_in_sort = copy.deepcopy(self.states)
        state_in_sort.append(max(self.states) + 1)
        state_in_sort.sort()
        for state in state_in_sort: # remove state1 and move other states forward one by one
            if state > state1:
                state_map["Q" + str(state - 1)] = copy.deepcopy(state_map["Q" + str(state)])
                state_map["Q" + str(state - 1)].index = state - 1
                del state_map["Q" + str(state)]
        ## program_sequence
        program_sequence.pop(state2 - 1)  # remove the statement related to state2
        loop_flag.pop(state2)


        # --------------------- modify accepted_states --------------------------- #
        self.accepted_states[0] = self.accepted_states[0] - 1


        # -------------------------- modify transition --------------------------- #
        # transfer the relations w.r.t state2 into state1's
        To_be_Added = []
        To_be_Removed = []
        for trans in self.transition:
            if trans[0] == state1 and trans[2] == state2:       # add self-loop
                To_be_Removed.append(trans)
                To_be_Added.append([state1, trans[1], state1])
            else:
                # adjust the index of states
                if trans[0] > state1:
                    trans[0] = trans[0] - 1
                if trans[2] > state1:
                    trans[2] = trans[2] - 1
        for item in To_be_Added:
            self.transition.append(item)
        for item in To_be_Removed:
            self.transition.remove(item)

    # for the potential loop, currently we only consider the non-nested while loop, need to update the following infos:
    # self, state_map, program_sequence
    def combine_loop(self, loops, guards, state_map, program_sequence):
        # loops = [[entry_state1, entry_state2], [entry_state1, entry_state2], ...] the combination of loop-entry
        # guards = [[guards, exit], [guards, exit], ...]   the above tuple's corresponding entry/exit statment
        while len(loops) != 0:
            [entry_state1, entry_state2] = loops.pop()    # do generalization in reverse
            [guard_statement, exit_statement] = guards[len(loops)]

            # -------------------------------------- modify states -------------------------------------- #
            To_be_removed = []
            To_be_added = []
            program_sequence_pop = []
            for state in self.states:
                if entry_state2 <= state < entry_state2 + (entry_state2 - entry_state1):    # unwanted loop-body
                    ## self
                    To_be_removed.append(state)
                    ## state_map
                    del state_map["Q" + str(state)]
                    ## program_sequence
                    program_sequence_pop.append(state - 1)
                elif state >= entry_state2 + (entry_state2 - entry_state1):                 # out of loop
                    ## self
                    To_be_removed.append(state)
                    To_be_added.append(state - (entry_state2 - entry_state1))
                    ## state_map
                    state_map["Q" + str(state - (entry_state2 - entry_state1))] = copy.deepcopy(state_map["Q" + str(state)])
                    state_map["Q" + str(state - (entry_state2 - entry_state1))].index = state - (entry_state2 - entry_state1)
                    del state_map["Q" + str(state)]
                    ## program_sequence
            ## program_sequence
            program_sequence_pop.sort(reverse=True)
            for i in program_sequence_pop:
                program_sequence.pop(i)
            ## self
            for item in To_be_removed:
                self.states.remove(item)
            for item in To_be_added:
                self.states.append(item)


            # -------------------------------------- modify accepted_states -------------------------------------- #
            self.accepted_states[0] = max(self.states)


            # ------------------------------------------- modify transition -------------------------------------- #
            To_be_Added = []
            To_be_Removed = []
            for trans in self.transition:
                # unwanted loop-body
                if entry_state2 <= trans[0] < entry_state2 + (entry_state2 - entry_state1) and entry_state2 <= trans[2] < entry_state2 + (entry_state2 - entry_state1):
                    To_be_Removed.append(trans)
                # before the unwanted loop-body
                elif trans[2] == entry_state2:
                    To_be_Removed.append(trans)
                    To_be_Added.append([entry_state2 - 1, guard_statement, entry_state1])
                # after the unwanted loop-body
                elif trans[0] == entry_state2 + (entry_state2 - entry_state1) -1:
                    To_be_Removed.append(trans)
                    To_be_Added.append([entry_state2 - 1, exit_statement, entry_state2])
                # other
                else:
                    # adjust the index of states
                    if trans[0] >= entry_state2 + (entry_state2 - entry_state1):
                        trans[0] = trans[0] - (entry_state2 - entry_state1)
                    if trans[2] >= entry_state2 + (entry_state2 - entry_state1):
                        trans[2] = trans[2] - (entry_state2 - entry_state1)
            for item in To_be_Added:
                self.transition.append(item)
            for item in To_be_Removed:
                self.transition.remove(item)



    # ---------------------------------- others -------------------------------------------------- #
    def show(self, name="trace_automata", flag=False):

        # name
        log = "FiniteAutomaton " + name + " = (" + "\n"

        # alphabet
        alphabet = ""
        for item in self.alphabet:
            alphabet = alphabet + item + " "
        alphabet = alphabet[0:-1]
        log += "\t alphabet = {" + alphabet + "}," + "\n"

        # states
        states = ""
        for item in self.states:
            states = states + "q" + str(item) + " "
        states = states[0:-1]
        log += "\t states = {" + states + "}," + "\n"
        log += "\t initialStates = {q0}," + "\n"

        # accepted_states
        accepted_states = ""
        for item in self.accepted_states:
            accepted_states = accepted_states + "q" + str(item) + " "
        accepted_states = accepted_states[0:-1]
        log += "\t finalStates = {" + accepted_states + "}," + "\n"

        # transitions
        log += "\t transitions = {" + "\n"
        for trans in self.transition:
            log += "\t \t (q" + str(trans[0]) + " " + trans[1] + " q" + str(trans[2]) + ")" + "\n"
        log += "\t }" + "\n"

        # end
        log += ");" + "\n"

        # print
        if flag: print(log)

        return log

    def visualization(self, dir={}):

        turtle.speed(8)
        # “fastest”: 0
        # “fast”: 10
        # “normal”: 6
        # “slow”: 3
        # “slowest”: 1

        width = 500
        height = 400

        margin = 2*width*0.9/(len(self.states)-1)

        state_location = {}
        for i in range(len(self.states)):
            if i == 0:
                state_location[0] = [-0.9*width, 0]
            elif i == len(self.states)-1:
                state_location[len(self.states) - 1] = [0.9*width, 0]
            else:
                state_location[i] = [np.random.randint(-0.9*width+(i-1)*margin, -0.9*width+i*margin, 1)[0], np.random.randint(-0.9*height, 0.9*height, 1)[0]]

        turtle.setup(2*width, 2*height, 0, 0)
        turtle.pensize(10)
        turtle.up()
        for i in range(len(self.states)):
            if i in self.accepted_states:
                turtle.pencolor("red")
            else:
                turtle.pencolor("blue")
            state = state_location[i]
            turtle.goto(state[0], state[1])
            turtle.down()
            turtle.goto(state[0], state[1])
            turtle.write("Q" + str(i), font=("Times", 18, "bold"))
            turtle.up()



        turtle.pensize(2)
        self_loop = {}
        for trans in self.transition:
            start = state_location[trans[0]]
            end = state_location[trans[2]]
            if start == end:  # self-loop
                if trans[0] in self_loop.keys():
                    self_loop[trans[0]] += 1
                else:
                    self_loop[trans[0]] = 1

                if trans[0] == max(self.states):
                    turtle.goto((start[0] + end[0]) / 2 - 80, (start[1] + end[1]) / 2 + 15 * self_loop[trans[0]])
                else:
                    turtle.goto((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + 15 * self_loop[trans[0]])
                turtle.write(dir[trans[1]], font=("Times", 15, "bold"))
            elif start > end: # potential loop
                turtle.pencolor("red")
                turtle.goto(start[0], start[1])
                turtle.down()
                turtle.goto(end[0] - np.random.random() * 10, end[1] - np.random.random() * 10)
                turtle.circle(5, steps=3)
                turtle.up()
                turtle.goto((start[0] + end[0]) / 2 - np.random.random() * 10,
                            (start[1] + end[1]) / 2 - np.random.random() * 10)
                # turtle.write(trans[1], font=("Times", 18, "bold"))
                turtle.write(dir[trans[1]], font=("Times", 15, "bold"))
                turtle.pencolor("black")
            else:
                turtle.pencolor("black")
                turtle.goto(start[0], start[1])
                turtle.down()
                turtle.goto(end[0] - np.random.random() * 10, end[1] - np.random.random() * 10)
                turtle.circle(5, steps=3)
                turtle.up()
                turtle.goto((start[0] + end[0])/2-np.random.random()*10, (start[1] + end[1])/2-np.random.random()*10)
                # turtle.write(trans[1], font=("Times", 18, "bold"))
                turtle.write(dir[trans[1]], font=("Times", 15, "bold"))

        turtle.hideturtle()

        # exit
        turtle.exitonclick()





if __name__ == "__main__":
    pass