#!/bin/bash

project_path=$(cd `dirname $0`; pwd)
cd $project_path


if [ -d ./RunExperiment0 ]; then
    rm -r RunExperiment*
fi


if [ -f ./fig.dat ]; then
    rm ./*.dat
    rm ./*.xlsx
fi

if [ -f ./final_result_log.txt ]; then
    rm ./final_result_log.txt
fi

