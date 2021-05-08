#!/bin/bash

project_path=$(cd `dirname $0`; pwd)
cd $project_path


if [ -f ./program.bpl ]; then
    rm ./*.bpl
fi

if [ -f ./program_tmp.ats ]; then
    rm ./*.ats
fi

if [ -f ./check_trace_property.tr ]; then
    rm ./check_trace_property.tr
fi