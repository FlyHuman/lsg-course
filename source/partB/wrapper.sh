#!/bin/sh

#Setting the environment variables

export JAVA_HOME=/usr
export SPARK_HOME=/cvmfs/softdrive.nl/lsg-crse/spark-2.0.1-bin-hadoop2.7
export PYTHONPATH=${SPARK_HOME}/python:$PYTHONPATH
export PATH=/cvmfs/softdrive.nl/lsg-crse/pbs-course-env/bin:$PATH
source activate course

# Printing node information

echo " The worker node running the script is:" ${HOSTNAME}
echo " The job is being run in the temporary directory:" ${TMPDIR}
echo " The job was submitted from the directory:" ${PBS_O_WORKDIR}

# Running zebrafish script

# For better performance, copy the script and execute it in the temporary directory
cd ${TMPDIR}
cp ${PBS_O_WORKDIR}/runfish/* .
# Create a random number in range {1 .. 10} as input argument
x=$(( ( RANDOM % 10 )  + 1 ))

# Run the actual script to calculate the principal components. The first argument is fixed and the second argument is random. 
python runFish.py 1 ${x}
# Exit the program in case of errors
if [[ "$?" != "0" ]]; then
    echo "Problem on runtime. Exiting now..."
    exit 1
fi

#Copying the output back to the directory where the job was submitted from

cp -r *.png ${PBS_O_WORKDIR}/

echo "Done!"
exit 0
