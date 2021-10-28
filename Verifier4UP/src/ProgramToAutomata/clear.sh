#!/bin/bash

project_path=$(cd `dirname $0`; pwd)
cd $project_path


if [ -f ./program.bpl ]; then
    rm ./*.bpl
fi

if [ -f ./program.ats ]; then
    rm ./*.ats
fi
