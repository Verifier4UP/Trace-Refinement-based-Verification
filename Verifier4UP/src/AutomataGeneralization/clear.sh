#!/bin/bash

project_path=$(cd `dirname $0`; pwd)
cd $project_path


if [ -f ./program.bpl ]; then
    rm ./*.bpl
fi

if [ -f ./trace_automata.ats ]; then
    rm ./*.ats
fi

if [ -f ./counter_example_trace.tr ]; then
    rm ./counter_example_trace.tr
fi