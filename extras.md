# LSG course 2016-11-22 - Extras

This is the Extras part of the Tutorial [LSG course](https://github.com/sara-nl/lsg-course/blob/master/README.md).

In this advanced part of our tutorial you can play around with a parallel processing technique on a shared-memory system. 
For this purpose, we will be running a Monte Carlo simulation to calculate an approximation of the value of π.

This exercise will let you run two programs, first with a serial implementation and then with an `openMP` parallel 
implementation of the simulation. The output of each program includes results for run time in wall-clock, user and system time.

Here are the steps:

1. [Prepare the pi application](#prepare-the-pi-application)
2. [Single-core jobs performance](#single-core-jobs-performance)
3. [Multicore jobs performance](#multi-core-jobs-performance)

### <a name="prepare-the-pi-application"></a> 1. Prepare the pi application

* Browse to the working directory. We will run the exercise in Extras:

```sh
cd ~/lsg-course/
cd extras/
```

* You should see the following files:

```sh
ls -l
```

> gridpi-mp-alt.c  
gridpi-serial.c  
Makefile   
wrapper_mp.sh  
wrapper_serial.sh

* Compile the `gridpi-serial.c` program:

```sh
gcc -std=c99 -Wall -Werror -pedantic gridpi-serial.c -o gridpi-serial
```

* Compile the `gridpi-mp-alt.c` program:

```sh
gcc -std=c99 -Wall -Werror -pedantic -fopenmp gridpi-mp-alt.c -lm -o gridpi-mp-alt
```

* You can run each program a few times on the UI, but depending on the current usage your runs
can take long (in that case move to the next section):

```sh
./gridpi-serial
```

```sh
./gridpi-mp-alt
```

* Open the wrapper scripts (`wrapper_serial.sh`, `wrapper_mp.sh`) and investigate the 
permissions for your executable (`chmod` command). Can you explain the reason that we set them 
in the wrapper?

### <a name="single-core-jobs-performance"></a> 2. Single-core jobs performance

#### Serial version 

* Submit the job to the cluster:

```sh
qsub -q stud_queue wrapper_serial.sh
```

#### Parallel version 

* Submit the job to the cluster:

```sh
qsub -q stud_queue wrapper_mc.sh
```

### <a name="multi-core-jobs-performance"></a> 3. Multi-core jobs performance

#### PBS directive

* Specify the number of cores to be allocated for your job:

`PBS -l nodes=1:ppn=2 # asks two cores on a single node`
 
* Submit the same jobs as previously and observe the performance for the following scenarios:
  * Edit the `ppn` value both in `wrapper_serial.sh` and `wrapper_mp.sh` to ask for 2 cores: `PBS -l nodes=1:ppn=2`. 
  * Edit the `ppn` value both in `wrapper_serial.sh` and `wrapper_mp.sh` to ask for 4 cores: `PBS -l nodes=1:ppn=4`. 

* Retrieve the output and observe the performance. Are the differences are significant? Can you explain?
 
> **HINT**: You can see the status of all your submitted jobs in a new terminal window with the use
of the command `watch qstat -u studXY`. Exit with `Ctrl+C`.
 
> You can perform multiple runs of each job, so that fluctuations caused by e.g. network can be middled out. 
 
> Can you think of other cases that you have to use multicore jobs? What happens if your program uses 
more memory than allocated to the cores that your job is reserving?
 
 
