# LSG course 2016-11-22 - Extras

This is the Extras part of the Tutorial [LSG course](https://github.com/sara-nl/lsg-course/blob/master/README.md).

**If you have not completed (and understood)** [Part A](https://github.com/sara-nl/lsg-course/blob/master/partA.md) 
and [Part B](https://github.com/sara-nl/lsg-course/blob/master/partB.md), please do so first.

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
ls
```

```sh
# gridpi-mp-alt.c  
# gridpi-serial.c  
# Makefile   
# wrapper_mp.sh  
# wrapper_serial.sh
```

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

> **_Food for brain:_**
>
> * Open the wrapper scripts (`wrapper_serial.sh`, `wrapper_mp.sh`) and investigate the 
permissions for your executable (`chmod` command). Can you explain the reason that we set them 
in the wrapper?

### <a name="single-core-jobs-performance"></a> 2. Single-core jobs performance

#### Serial version 

* Submit the job to the cluster:

```sh
qsub -q stud_queue wrapper_serial.sh
```

* Monitor the job progress and inspect the output file of the serial run when available.

#### Parallel version 

* Submit the job to the cluster:

```sh
qsub -q stud_queue wrapper_mp.sh
```

* Monitor the job progress and inspect the output file of the parallel run when available.

### <a name="multi-core-jobs-performance"></a> 3. Multi-core jobs performance

#### PBS directive

* You can specify the number of cores to be allocated for your job by including this line in your job script: `PBS -l nodes=1:ppn=2`. Here we asks two cores on a single node. Find this line in your `wrapper_serial.sh` and `wrapper_mp.sh` scripts.
 
* For the following scenarios, submit the same jobs again and observe the performance :
  * Edit the `ppn` value both in `wrapper_serial.sh` and `wrapper_mp.sh` to ask for 2 cores: `#PBS -l nodes=1:ppn=2`. 
  * Edit the `ppn` value both in `wrapper_serial.sh` and `wrapper_mp.sh` to ask for 4 cores: `#PBS -l nodes=1:ppn=4`. 

* Retrieve the output and observe the performance. Are the differences significant? Can you explain?
 
> **_Food for brain:_**
>
> * You can see the status of all your submitted jobs in a new terminal window with the use
of the command `watch qstat -u studXY`. Exit with `Ctrl+C`.
* You can perform multiple runs of each job, so that fluctuations caused by e.g. network can be middled out. 
* Can you think of other cases that you have to use multicore jobs? What happens if your program uses 
more memory than allocated to the cores that your job is reserving?
 
 
