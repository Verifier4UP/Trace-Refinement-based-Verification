#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random

# trival one
pattern0 = "\tif (s == r0) {\n" \
           "\t\tx := f(x);\n" \
           "\t\ty := f(y);\n" \
           "\t}\n\n"

# earlyassumes
pattern1 = "\tif (s == u1) {\n" \
           "\t\tx := f(t);\n" \
           "\t\ty := f(k);\n" \
           "\t\tassume(t == k);\n" \
           "\t\tx := h(x);\n" \
           "\t\ty := h(y);\n" \
           "\t}\n\n"

# non-earlyassumes
pattern2 = "\tif (s == v2) {\n" \
           "\t\tx := f(t);\n" \
           "\t\ty := f(k);\n" \
           "\t\tx := h(x);\n" \
           "\t\ty := h(y);\n" \
           "\t\tassume(t == k);\n" \
           "\t}\n\n"

# memorizing
pattern3 = "\tif (s == u3) {\n" \
           "\t\tx := f(x);\n" \
           "\t\ty := f(y);\n" \
           "\t\tx := h(x);\n" \
           "\t\ty := h(y);\n" \
           "\t}\n\n"

# non-memorizing
pattern4 = "\tif (s == v4) {\n" \
           "\t\tx := f(x);\n" \
           "\t\tx := h(x);\n" \
           "\t\ty := f(y);\n" \
           "\t\ty := h(y);\n" \
           "\t}\n\n"

# non-coherence while
pattern5 = "\tif (s == u5) {\n" \
           "\t\tx := t;\n" \
           "\t\ty := k;\n" \
           "\t\twhile (y != z){\n" \
           "\t\t\tx := f(x);\n" \
           "\t\t\ty := f(y);\n" \
           "\t\t\tz := f(z);\n" \
           "\t\t}\n" \
           "\t\tassume(t == k);\n" \
           "\t}\n\n"


# coherence while
pattern6 = "\tif (s == v6) {\n" \
           "\t\tx := t;\n" \
           "\t\ty := k;\n" \
           "\t\tassume(t == k);\n" \
           "\t\twhile (y != z){\n" \
           "\t\t\tx := f(x);\n" \
           "\t\t\ty := f(y);\n" \
           "\t\t\tz := f(z);\n" \
           "\t\t}\n" \
           "\t}\n\n"

# nested while
pattern7 = "\tif (s == u7) {\n" \
           "\t\twhile (w1 != w2) {\n" \
           "\t\t\tif (w3 == w4) {\n" \
           "\t\t\t\tx := f(x);\n" \
           "\t\t\t\ty := f(y);\n" \
           "\t\t\t\tw3 := l(w3);\n" \
           "\t\t\t\tassume(w3 != w4);\n" \
           "\t\t\t} else {\n" \
           "\t\t\t\tx := h(x);\n" \
           "\t\t\t\ty := h(y);\n" \
           "\t\t\t\tw4 := l(w4);\n" \
           "\t\t\t\tassume(w3 == w4);\n" \
           "\t\t\t}\n" \
           "\t\t\tw1 := f(w1);\n" \
           "\t\t}\n" \
           "\t}\n\n"


def generator_benchmark(max_block=3):

    correctness = True

    pattern = [pattern0, pattern1, pattern2, pattern3, pattern4, pattern5, pattern6, pattern7]
    var_dir = {pattern0: ["x", "y", "s", "r0"],
               pattern1: ["x", "y", "t", "k", "s", "u1"],
               pattern2: ["x", "y", "t", "k", "s", "v2"],
               pattern3: ["x", "y", "s", "u3"],
               pattern4: ["x", "y", "s", "v4"],
               pattern5: ["x", "y", "z", "t", "k", "s", "u5"],
               pattern6: ["x", "y", "z", "t", "k", "s", "v6"],
               pattern7: ["x", "y", "s", "u7", "w1", "w2", "w3", "w4"]
               }
    func_dir = {pattern0: ["f"],
                pattern1: ["f", "h"],
                pattern2: ["f", "h"],
                pattern3: ["f", "h"],
                pattern4: ["f", "h"],
                pattern5: ["f"],
                pattern6: ["f"],
                pattern7: ["f", "h", "l"]
                }

    n = 0
    context_declare_var = []
    context_declare_func = []
    context_main = "\tx := y;\n\n"



    while n < max_block and len(pattern) != 0:
        select = random.randint(0, len(pattern)-1)
        select_pattern = pattern.pop(select)

        if select_pattern == pattern7:
            if set([pattern2, pattern4, pattern5]) < set(pattern):
                pattern.remove(pattern2)
                pattern.remove(pattern4)
                pattern.remove(pattern5)
            else:
                break
        elif select_pattern in [pattern2, pattern4, pattern5] and pattern7 in pattern:
            pattern.remove(pattern7)

        context_declare_var += var_dir[select_pattern]
        context_declare_func += func_dir[select_pattern]
        context_main += select_pattern

        # Consider whether to add branches
        elif_choice = random.randint(0, 2)
        if elif_choice == 0 and len(pattern) != 0:
            else_select = random.randint(0, len(pattern) - 1)
            else_select_pattern = pattern.pop(else_select)
            context_declare_var += var_dir[else_select_pattern]
            context_declare_func += func_dir[else_select_pattern]
            context_main = context_main[0:-2] + " else {\n" + \
                           "\t\t" + else_select_pattern.replace("\n\t", "\n\t\t\t")[0:-2] + "\n" + \
                           "\t}\n\n"
        elif elif_choice == 1:
            context_main = context_main[0:-2] + " else {\n" + \
                           "\t\tx := f(x);\n" + \
                           "\t}\n\n"
            context_declare_func.append("f")
            correctness = False
        elif elif_choice == 2:
            context_main = context_main[0:-2] + " else {\n" + \
                           "\t\tx := f(x);\n" + \
                           "\t\ty := f(y);\n" + \
                           "\t}\n\n"
            context_declare_func.append("f")
        n += 1

    with open("./benchmark-program.bpl", 'w') as f:

        # Declare the program
        f.write("type A;\n")
        context_declare_func = list(set(context_declare_func))
        context_declare_func.sort()
        for item in context_declare_func:
            f.write("function " + item + "(x: A) returns (A);\n")
        f.write("procedure main(){\n\n")

        context_declare_var = list(set(context_declare_var))
        context_declare_var.sort()
        var = "\tvar "
        for item in context_declare_var:
            var = var + item + ", "
        var = var[0:-2] + ": A;\n\n"
        f.write(var)

        # Determine the main body of the program
        f.write(context_main)

        # assertion
        f.write("\tassert(x == y);\n}")

    return correctness


if __name__ == "__main__":

    correctness = generator_benchmark()
    print(correctness)


