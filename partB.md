# LSG course 2016-11-22 - part B

This is part B of the Tutorial [LSG course](https://github.com/sara-nl/lsg-course/blob/master/README.md). Here you will run an application 
that shows you the benefit of using the LSG cluster. 

**If you have not completed (and understood)** [Part A](https://github.com/sara-nl/lsg-course/blob/master/partA.md), please do so first.

Here are your next steps:

1. [Run the Fish application](#run-the-fish-application)
2. [Submit multiple jobs](#submit-multiple-jobs)
3. [Build your job](#build-your-job)

#### <a name="run-the-fish-application"></a> 1. Run the Fish application

We have adapted [some code](https://github.com/spark-mooc/mooc-setup/blob/master/ML_lab5_pca_student.ipynb) from an example where they are working with [larval zebrafish](http://research.janelia.org/zebrafish/), so that you can run it on the LSG cluster. 

It outputs a picture showing the PCA analysis of the 2 principal components that you choose, for a given fish's neural system's activity in time, in response to certain stimulii. 

* Browse to the working directory. We will run the Fish exercise in partB:

```sh
cd ~/lsg-course/
cd partB/
ls
```

* Let's submit the job to the cluster

```sh
qsub -q stud_queue wrapper.sh

# 6402.gb-ce-kun.els.sara.nl
```
  
* Monitor the progress of your job 

```sh
qstat 6402   # replace 6402 with your jobID
```

> **_Food for brain:_**
>
> * Uhm... did it really take that little to finish? Run the following command: `qstat`
* What do you see? What does it mean?
  
* The output of jobs is placed in the directory where the submit command was issued. And we get the (already familiar) .e... and .o... files as well. In our fishes example, we expect the program to produce a `.png` file containing a fish image. Is it there? Check:

```sh
ls

# runfish  
# wrapper.sh  
# wrapper.sh.e6402  
# wrapper.sh.o6402  
```

* So... unfortunately, we cannot see the `.png` file. We can see the .e... and .o... files though. Open the `wrapper.sh.e**` and `wrapper.sh.o**` files. Do you understand what went wrong?  

> **_Food for brain:_**
>
> * Which of the .e... and .o... files tells you that something went wrong? 
* Which of the .e... and .o... files tells you what went wrong? 
* The file you answer in the previou question is actually showing you a Python error telling you that the program failed to run properly because it could not import a module called pyspark.sql. Pyspark is a Python module that is not just simply available by default for everybody in the cluster. Therefore, if you want to use it, you have to let your running environment know where it can find that module. In particular, to illustrate a job failure, we have (deliberately) written a wrong path to this module on the wrapper.sh file. Mistyping a path is a common problem that could easily happen to you, though, when you are defining your jobs. Open the `wrapper.sh` script. Can you find where the path to this _extra_ software is specified?
* Based on your previous answer, can you actually see where the software is installed? Then, what do you think: is it installed locally on the cluster or is it somewhere else? 
* Oh, and can you answer the previous two questions now for the input dataset?
 
* In the `wrapper.sh`, the environment variable SPARK_HOME should point to the **absolute path** of the Pyspark module, but the initial slash (`/`) is missing. Correct this, save the script and submit the job again. 

* Check the status of the job with the new jobID
 
* Once the job has successfully finished execution, display the image:

```sh
display PC1-2.png  # replace with your own PC1-*.png file
```

* In case this does not work or if you want to copy the output image to your laptop, do the following: 
  * Start a new terminal window in your laptop (but do **not** log in to the cluster in it).  
  * Type the following command to download the picture to your laptop:

  ```sh
  scp "studXY@gb-ui-kun.els.sara.nl:/home/studXY/lsg-course/partB/*.png" .  # replace `studXY` with your username
  ```
   
    * Windows users should run the following command to get the image on their Desktops:
    
    ```sh
    cp *.png /c/Users/maithili/Desktop/ # replace `maithili` with your the username you have in your laptop
    ```
    
  * You can now display the fish picture using any image viewer in your laptop (any web browser will also do fine).

### <a name="submit-multiple-jobs"></a> 2. Submit multiple jobs

#### Array jobs

* It is possible to launch many jobs (or array jobs) with one single 'qsub' command:

```sh
qsub -q stud_queue -t 1-4 wrapper.sh 

# 6401[].gb-ce-kun.els.sara.nl
```

#### Advanced functions 

* Lists all of your current jobs:

```sh
qstat -u studXY  # Replace studXY with your username 
```

* Get details of each job (in this case the array index is between 1 to 4): 

```sh
qstat -f 6401[1]   # Replace 6401[1] with your jobID
```

* List all running jobs per worker node:

```sh
pbsnodes       
```

* What if you realise that your running job is not correct. You can cancel a submitted job with:

```sh
qdel 6401      
```

> **_Food for brain:_**
>
> * How can you cancel a single array job or the whole array? Can you remove some of the array jobs?


### <a name="build-your-job"></a> 3. Build your job

#### PBS environment variables

In a job, PBS defines a number of directives to help the cluster scheduler find the best-suited resources. 
You can set the `PBS directives` at the beginning of your job script (starting with `#PBS`).

* **Walltime:** For how long will the sysem wait to run your job? Specify the maximum job walltime 
in hh:mm:ss by adding this line at the beginning of your `wrapper.sh` script:
 
```sh
#PBS -l walltime=4:00:00 # the job will run 4h at maximum
```

* **Cores:** How many cores does your job need to run? Specify the number of cores to be allocated for your 
job:

```sh
#PBS -l nodes=1:ppn=2 # asks two cores on a single node
```

#### Queues explained

* On the LSG clusters you can find different queues: 

```sh
# =============== ===========================
# Queue           Max. Walltime (hh:mm:ss)
# =============== ===========================
# express         00:30:00
# medium          36:00:00
# long            72:00:00
# =============== ===========================
```

* You can specify your queue when you submit the job:
 
```sh
qsub -q long wrapper.sh # allow job to run for 72 hours
```
   
> **_Food for brain:_**
>
> * Think of a program you are currently running for your research, and imagine that all software is already installed and accessible to you somewhere in the cluster. Can you sketch the steps that you would need to follow to create your own job script?
* Play around, submit few jobs and try to adapt your own programs. 
