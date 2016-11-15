# LSG course 2016-11-22 - part B

This is part B of the Tutorial [LSG course](https://github.com/sara-nl/lsg-course/blob/master/README.md). Here you will run an application 
that shows you the benefit of using the LSG cluster. 

**If you have not completed (and understood)** [Part A](https://github.com/sara-nl/lsg-course/blob/master/partA.md), please do so first.

Here are your next steps:

1. [Run the Fish application](#run-the-fish-application)
2. [Submit multiple jobs](#submit-multiple-jobs)
3. [Queues explained](#queues-explained)

#### <a name="run-the-fish-application"></a> 1. Run the Fish application

* Browse to the working directory. We will run the Fish exercise in partB:

```sh
cd ~/lsg-course/
cd partB/
```

* Let's submit the job to the cluster

```sh
qsub -q stud_queue wrapper.sh
```

>6402.gb-ce-kun.els.sara.nl
  
* Monitor the progress of your job 

```sh
qstat 6402   # replace 6402 with your jobID
```

* Run the following command:

```sh
qstat
```
  
What do you see? What does it mean?
  
* Once the job is ready, check your output:

```sh
ls
```
 
>
runfish  
wrapper.sh  
wrapper.sh.e6402  
wrapper.sh.o6402  


> What does the `wrapper.sh.e**` file say?  
> Where is the software installed? Is it local on your cluster or elsewhere? Where is the input dataset?
> **Hint:** The path to the software was not given correctly, so the job failed to run the example properly and generate the output. 
In the wrapper.sh the variable name SPARK_HOME points to a wrong absolute path (the slash `/` was missing). 

* Correct the path in `wrapper.sh`, save the script and submit the job again. 

* Check the status of the job with the new jobID
 
* Once the job has successfully finished execution, display the result:

```sh
display PC1-2.png
```

In case this does not work, you can copy the file locally on your laptop and then view it. 
* Start a new terminal window and type

```sh
scp studXY@gb-ui-kun.els.sara.nl:/home/studXY/lsg-course/partB/PC1-2.png .  # replace `studXY` with your username
```

### <a name="submit-multiple-jobs"></a> 2. Submit multiple jobs

#### Array jobs

* It is possible to launch many jobs (or array jobs) with one single 'qsub' command:

```sh
qsub -q stud_queue -t 1-4 wrapper.sh 
```

#### Advanced functions 

* Get details of the jobID: 

```sh
qstat -f 6401   # Replace 6401 with your jobID
```

* Lists your current jobs:

```sh
qstat -u studXY  # Replace studXY with your username 
```

* Cancel a submitted job:

```sh
qdel 6401      
```

* List all the running/queued jobs in the cluster:

```sh
qstat          
```  

List all running jobs per worker node:

```sh
pbsnodes       
```

### <a name="queues-explained"></a> 3. Queues explained

**Walltime** For how long will the sysem wait to run your job? Specify the maximum job walltime in hh:mm:ss in wrapper.sh
 .. code-block:: console
 
```sh
PBS -l walltime=4:00:00 # the job will run 4h at maximum
```

**Local queues** On the LSG clusters you can find different queue types. 

```sh
=============== ===========================
Queue           Max. Walltime (hh:mm:ss)
=============== ===========================
express         00:30:00
infra           00:30:00
medium          36:00:00
long            72:00:00
=============== ===========================
```

This can be specified with the following command
 
```sh
qsub -q long wrapper.sh # allow job to run for 72 hours
```
   
   
