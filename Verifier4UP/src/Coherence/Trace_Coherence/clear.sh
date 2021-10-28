#!/bin/bash

project_path=$(cd `dirname $0`; pwd)
cd $project_path

if [ -f ./trace_origin.tr ]; then
    rm ./*.tr
fi