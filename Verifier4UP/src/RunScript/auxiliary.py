#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from env_setup import root_path

# ----------------------------------------------------- auxiliary func ---------------------------------------- #
# Count the number of lines of code
def LoC(boogie_file):
    env_setting = "export PATH=" + root_path + "cloc:$PATH;"
    c_program = boogie_file[:boogie_file.rfind(".bpl")] + ".c"
    os.system("cp " + boogie_file + " " + c_program)
    result = os.popen(env_setting + "cloc " + c_program).read()
    result = result.split("\n")
    os.system("rm " + c_program)
    for line in result:
        if "C        " in line:
            return line.split()[-1]



if __name__ == "__main__":
   pass