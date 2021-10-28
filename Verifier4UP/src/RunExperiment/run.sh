#!/bin/bash

time_threshold=$1
Nproc=$2
total_mission=$3
folder=$4


# ----------------------------------------------------------------------------------#
#time_threshold=1200

# --------------------------------- self-designed --------------------------------- #
#Nproc=6			                                # the limit number of processes
#total_mission=6	                                # the number of missions
#folder="../ArtifactBenchmark/self-designed/"    # the dirs

# --------------------------------------- svcomp ---------------------------------- #
#Nproc=6		                            # the limit number of processes
#total_mission=44	                        # the number of missions
#folder="../ArtifactBenchmark/svcomp/"       # the dirs

# --------------------------------------- SLL ------------------------------------- #
#Nproc=6			                            # the limit number of processes
#total_mission=48	                        # the number of missions
#folder="../ArtifactBenchmark/SLL/"          # the dirs

# --------------------------------------- TREE ---------------------------------- #
#Nproc=4			                            # the limit number of processes
#total_mission=4	                            # the number of missions
#folder="../ArtifactBenchmark/TREE/"         # the dirs

# ---------------------------------------- error ---------------------------------- #
#Nproc=1			                                # the limit number of processes
#total_mission=2 	                            # the number of missions
#folder="../ArtifactBenchmark/error_test/"       # the dirs









# ----------------------------------------------------------------------------------#

#mission
function mission_ours(){
	cd RunExperiment$[$1-1]
	python3 script.py Obj "ours" $time_threshold
}
function mission_ultimate(){
	cd RunExperiment$[$1-1]
	python3 script.py Obj "ultimate" $time_threshold
}



function tool_ours(){
    echo "------------------------------using ours--------------------------------"
    echo `date "+%Y-%m-%d %H:%M:%S"`

    Pfifo="/tmp/$$.fifo"    # create a fifo type file
    mkfifo $Pfifo     		# create a named pipe
    exec 6<>$Pfifo     		# fd is 6
    rm -f $Pfifo

    # Initialize the pipe
    for((i=1; i<=$Nproc; i=i+1)); do
        echo
    done >&6


    for ((j=1; j<=$total_mission; j=j+1))
    do
        read -u6
        {
            echo mission $[$j-1]
            mission_ours $j
            echo mission $[$j-1] completed.
            echo >&6
        } &
    done

    wait     # waiting for all the background processes finished
    echo `date "+%Y-%m-%d %H:%M:%S"`
}


function tool_ultimate(){
    echo "------------------------------using ultimate--------------------------------"
    echo `date "+%Y-%m-%d %H:%M:%S"`

    Pfifo="/tmp/$$.fifo"    # create a fifo type file
    mkfifo $Pfifo     		# create a named pipe
    exec 6<>$Pfifo     		# fd is 6
    rm -f $Pfifo

    # Initialize the pipe
    for((i=1; i<=$Nproc; i=i+1)); do
        echo
    done >&6


    for ((j=1; j<=$total_mission; j=j+1))
    do
        read -u6
        {
            echo mission $[$j-1]
            mission_ultimate $j
            echo mission $[$j-1] completed.
            echo >&6
        } &
    done

    wait     # waiting for all the background processes finished
    echo `date "+%Y-%m-%d %H:%M:%S"`
}



# ----------------------------------------------------------------------------------#
# set the folder for each mission
for((i=0; i<=$[$total_mission-1]; i=i+1));
do
    if [ -d ./RunExperiment$i ];then
        rm -r ./RunExperiment*
    fi
    cp -r ../RunScript ./RunExperiment$i
    mkdir ./RunExperiment$i/Obj
done

files=$(ls $folder)
num=0
for file in $files
do
    if [ -f $folder$file ];then
        flag=$(($num % $total_mission))
        cp $folder$file ./RunExperiment$flag/Obj
        num=$[$num+1]
    fi
done


tool_ours
tool_ultimate

