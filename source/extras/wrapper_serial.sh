#!/bin/sh
#PBS -l nodes=1:ppn=1 

# Printing node information

echo " The worker node running the script is:" ${HOSTNAME}
echo " The job is being run in the temporary directory:" ${TMPDIR}
echo " The job was submitted from the directory:" ${PBS_O_WORKDIR}

# Running pi script

# For better performance, copy the script and execute it in the temporary directory
cd ${TMPDIR}
cp ${PBS_O_WORKDIR}/gridpi-serial .

# Set the proper permissions
chmod u+x gridpi-serial

# Run the actual script to calculate the pi approximation.
./gridpi-serial
# Exit the program in case of errors
if [[ "$?" != "0" ]]; then
    echo "Problem on runtime. Exiting now..."
    exit 1
fi

echo "Done!"
exit 0
