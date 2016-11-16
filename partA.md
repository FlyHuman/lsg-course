# LSG course 2016-11-22 - part A

This is part A of the Tutorial [LSG course](https://github.com/sara-nl/lsg-course/blob/master/README.md).

Here are your first steps:

1. [Access the user interface](#access-the-user-interface)
2. [My first job](#my-first-job)
3. [Get job status and output](#get-job-status-and-output)

### <a name="access-the-user-interface"></a> 1. Access the User Interface

The UI (short for User Interface) is the login node that allows you to interact with the LSG. Let's log in.

#### Log in to the UI

* Open a terminal in your laptop
* Login to the "kun" cluster UI located in Nijmegen:
  * Your username is **studXY**, replace `XY` with the number assigned to you.
  * You will receive the password from the workshop facilitators.

```sh
ssh -X studXY@gb-ui-kun.els.sara.nl  
```

#### Get familiar with the UI 

* Find your home directory and its content:

```sh
pwd

ls -l
```

* On your home directory, you have a directory called `lsg-course`, within it another three called partA, 
partB and exras. List the content of the working directory where the exercises are located:

```sh
ls -R lsg-course/
```

> You should see the output: 
```sh
# lsg-course/:
# extras  partA  partB
# 
# lsg-course/extras:
# gridpi-mp-alt.c  Makefile  wrapper_serial.sh  gridpi-serial.c  wrapper_mp.sh
# 
# lsg-course/partA:
# hello.sh
# 
# lsg-course/partB:
# runfish  wrapper.sh
# 
# lsg-course/partB/runfish:
# runFish.py
```

### <a name="my-first-job"></a> 2. My first job 

#### Run the script on the UI

* Browse to the working directory. We will run first the exercise in partA:

```sh
cd ~/lsg-course/
cd partA/
ls
```

* Let's run your first script!

```sh
./hello.sh
```

* Let's change the script to say hello 'your-name':

```sh
nano hello.sh
```

>Run the script again. What does it say?

#### Run the script on the cluster

* So shall we run the same example on the cluster?

```sh
qsub -q stud_queue hello.sh
```

* This command returns a unique jobID (e.g., here it is 6401). Find your own:

```sh
# 6401.gb-ce-kun.els.sara.nl
```

This is the identification of the job that can be used to monitor the progress of the job, as shown in next section.

### <a name="get-job-status-and-output"></a> 3. Get job status and output

#### Monitor the progress 

* Monitor the progress of your job using this jobID

```sh 
qstat 6401   # replace 6401 with your jobID
```

You should see something like this:

```sh
# Job ID                    Name             User            Time Use S Queue
# ------------------------- ---------------- --------------- -------- - -----
# 6401.gb-ce-kun            hello.sh         stud23          00:00:00 R stud_queue 
```  

* Get more details about the job:

```sh 
qstat -f 6401 
```

#### Retrieve the output

* Once the job is ready the status will be:

```sh
qstat 6401
# qstat: Unknown Job Id Error 6401.gb-ui-kun.els.sara.nl
```  

* This suggests that the job is done. What is your output?

```sh  
  ls
```

You should see two new files in your directory:

```sh
# hello.sh
# hello.sh.e6401
# hello.sh.o6401
```

#### What happened?

Congratulations! You have just run your first job on the LSG cluster!

> **_Food for brain:_**
>
> * What information is in the `hello.sh.e6401` and `hello.sh.o6401` files?
* How can you tell that your job run on the cluster and not on the UI?
* Make a small change in the script and run the job again. Inspect the output files.


