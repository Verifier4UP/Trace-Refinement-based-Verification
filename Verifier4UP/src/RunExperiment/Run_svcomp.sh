#!/bin/bash

# usage: ././run.sh time_threshold Nproc total_mission folder

if [ -d ./collect-svcomp-1-600 ];then
    rm -r ./collect-svcomp-1-600
    rm collect-svcomp-1-600.xlsx
fi
./run.sh 600 1 46 ../../../ArtifactBenchmark/svcomp/
python3 collect.py collect-svcomp-1-600.xlsx
mkdir collect-svcomp-1-600
mv  RunExperiment* ./collect-svcomp-1-600
cp collect-svcomp-1-600.xlsx ./collect-svcomp-1-600
echo -e "\n\n\n"
python3 latex.py collect-svcomp-1-600.xlsx False True
cp fig.dat ./collect-svcomp-1-600
mv fig.dat fig_svcomp.dat