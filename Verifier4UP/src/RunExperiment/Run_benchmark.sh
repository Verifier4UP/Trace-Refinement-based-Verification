#!/bin/bash

# usage: ././run.sh time_threshold Nproc total_mission folder

if [ -d ./collect-benchmark-1-600 ];then
    rm -r ./collect-benchmark-1-600
    rm collect-benchmark-1-600.xlsx
fi
./run.sh 600 1 50 ../../../ArtifactBenchmark/benchmark/
python3 collect.py collect-benchmark-1-600.xlsx
mkdir collect-benchmark-1-600
mv  RunExperiment* ./collect-benchmark-1-600
cp collect-benchmark-1-600.xlsx ./collect-benchmark-1-600
echo -e "\n\n\n"
python3 latex.py collect-benchmark-1-600.xlsx False False
cp fig.dat ./collect-benchmark-1-600
mv fig.dat fig_benchmark.dat