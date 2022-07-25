#### How many statuses are in a job(in the code for this report—scheduler)? And what are they? 本次实验作业有几种状态(在本次报告的代码中-scheduler)？请列举

```C

```



#### What programs for job control are used in this experiment? And their function? 本实验作业控制命令处理程序包括哪些？它们分别实现什么功能？

```c

```



#### What is used for inter-process communication in this experiment? And its function? 本实验采用什么进行进程之间的通信？它相当于什么作用？

A file. `enq.c`, `deq.c` and `stat.c` write down the command into the file in `/tmp/shedule.fifo`. And then `scheduler.c` read command from this file when `schedule()` is triggered by `SIGVTALRM` or `SIGCHLD`. 

Its function is building connection between `scheduler` and `enq`, `deq` and `stat` for sending command to scheduler. This function is similar to shared-memory in inter-process communication.



#### What should be noted when printing out the job name: 在打印出作业名称的时候应该注意什么问题:

1. A selected but not yet executed job is not in the queue so that it MIGHT not be printed. This should be noted.

2.  The format should be noted: "%d\t%d\t%s\t%d\t%d\t%d\t%d\t%d\t%s\t%s\n"
   1. The string should end with '\0' and be represented by "%s".



#### Submit a job that takes more than 100 milliseconds to run（pleas paste your code）: 提交一个运行时间超过100毫秒的作业（请直接粘贴代码）:

// task.c

```C
// Fibonacci - O(2^n) version
int f(int n);

int main(){
    int i = 0;
    for(i = 0; i < 38; ++i){
        f(i);
    }
    return 0;
}

int f(int n){
    if(n < 1)
        return 0;
    if(n == 1 || n == 2)
        return 1;
    else
        return f(n - 1) + f(n - 2);
}
```





#### List the bugs you found and your fix(Describe the cause of bugs in detail and how to modify it)：列举出你找到的bug并给出你的解决方案（请仔细描述bug的原因以及修复方案）：

**BUG 1** compile failed.

description: Bad coding

location : Line 84

```C
p->job->wait_time += 1ï¼›
```

Fixed: 

```C
p->job->wait_time += 1;
```



**BUG 2** cannot add more than three jobs

description: cannot print status if more than three tasks added because <u>a loop is formed</u> in queue.

![Infinite loop](https://s1.ax1x.com/2020/03/30/GmVGex.jpg)

location: jobselect()

Fixed: remove the next pointer before dequeue a node.

```C
if(select){
	select->next = NULL;
}
```

location: jobselect(), do_que()

```C
if (select == selectprev && head != NULL) head = NULL;
```

Fixed: head should not be assigned to NULL directly if head is the node should be dequeued.

```C
if (select == selectprev && head != NULL) head = head->next;
```



**BUG 3** wrong time slice

description: the interval is set to 0:000100s

location: main()

```C
interval.tv_sec = 0;
interval.tv_usec = 100;
```

Fixed: make it 100ms

```C
interval.tv_sec = 0;
interval.tv_usec = 100000;
```



**BUG 4** Danger!!

description: access NULL

location: do_deq()

```C
for (prev = head, p = head; p != NULL; prev = p, p = p->next) {
	if (p->job->jid == deqid) {
		select = p;
		selectprev = prev;
		break;
	}
}					
selectprev->next = select->next;
```

Fixed: judge before access

```C
if(select){
	selectprev->next = select->next;
}else{
	return;
}
```



**BUG 5** current job stops forever

description: the new job would never be run if the `jobselect()` and `jobswitch()` are called before `raise(SIGSTOP)` and this new job is selected and assigned to  `current` and `SIGCONT` is sent to the `current`.  After that, `raise(SIGSTOP)` is executed. 

Then... This job can stop forever.

location: do_enq()

```C
if (pid == 0) {	
	newjob->pid = getpid();	
	/* block the child wait for run */
	raise(SIGSTOP);
    ....
```

Fixed: go to jobswitch() and send `SIGCONT` to current job if no job is waiting to`make sure the `current` job will be run.

```C
} else {    /* next == NULL && current != NULL, no switch */
	kill(current->job->pid, SIGCONT);
	return;		
}
```









#### Run the job scheduler program, And analyze the execution of the submitted job: 运行作业调度程序，分析提交作业后的作业的执行过程:


![](https://s1.ax1x.com/2020/03/30/GmVNFO.jpg)



1. A enq command is written into `/tmp/scheduler.fifo`.
2. Scheduler is triggered by `SIGVTALRM` signal, call `schedule()` function.

3. `scheduler()` call `do_enq()` function.
4. The details of job is parsed and then a child process is forked. The child process stop immedietaly since `SIGSTOP` is raised.
5. `updateall()` is called to update the running time, waiting time and current priority of jobs.
6. `jobselect()` is called to select the new job and let `next` point to it.
7. `jobswitch()` is called to send a `SIGCONT` to the job waiting, and send a `SIGSTOP` to the current running job and put it back to the queue.
8. The child process part in `de_enq()` resumes, and run `execv()` to execute the job.



#### Understand the process of job scheduling——Submit a new job (Execution results and corresponding code)： Schedueler作业调度的过程理解——提交新作业 （执行结果及代码表现）： 

1. The arguments of `enq` are parsed and warpped into a `jobcmd` structure.

   ```C
   enqcmd.type = ENQ;
   	enqcmd.defpri = p;
   	enqcmd.owner = getuid();
   	enqcmd.argnum = argc;
   	offset = enqcmd.data;
   	
   	while (argc-- > 0) {
   		strcpy(offset,*argv);
   		strcat(offset,":");
   		offset = offset + strlen(*argv) + 1;
   		argv++;
   	}
   ```

2. The `jobcmd` carrying the information to start a new job is written into a file

   ```C
   if ((fd = open(FIFO,O_WRONLY)) < 0)
   	error_sys("enq open fifo failed");
   	
   if (write(fd,&enqcmd,DATALEN)< 0)
   	error_sys("enq write failed");
   	
   close(fd);
   ```

3. A virtual alarm signal is received by `scheduler` and a customized handler is called, and `schedule()` is called due to the `SIGVTALRM` signal.:

   ```C
   void sig_handler(int sig, siginfo_t *info, void *notused)
   {
   	int status;
   	int ret;
   	
   	switch (sig) {
   	case SIGVTALRM:
   		schedule();
               
       ......
   ```

4. `schedule()` : read a new command from the file

   ```C
   bzero(&cmd, DATALEN);
   if ((count = read(fifo, &cmd, DATALEN)) < 0)
   	error_sys("read fifo failed");
   ```

5. `schedule()` : the command is ENQ, call `do_enq()`

   ```C
   case ENQ:
   	do_enq(newjob,cmd);
   	break;
   ```

6. `do_enq()` : the information about the new job is parsed

   ```C
   newjob = (struct jobinfo *)malloc(sizeof(struct jobinfo));
   newjob->jid = allocjid();
   newjob->defpri = enqcmd.defpri;
   newjob->curpri = enqcmd.defpri;
   newjob->ownerid = enqcmd.owner;
   ......
   ```

7. `do_enq()` : the new job is enqueued

   ```C
   enqueue(newnode);
   ```

8. `do_enq()` : a child process is forked. 

   ```C
   if ((pid = fork()) < 0)
   	error_sys("enq fork failed");
   ```

9. `do_enq()` : the child process halts immedietely since a `SIGSTOP` is raised.

   ```C
   raise(SIGSTOP);
   ```

10. `do_enq()` : the child process waits for a `SIGCONT`. if a `SIGCONT ` is received, execute the job:

    ```C
    dup2(globalfd,1);
    if (execv(arglist[0],arglist) < 0)
    	printf("exec failed\n");
    exit(1);
    ```

    



#### Understand the process of job scheduling——End of job execution (Execution results and corresponding code)： Schedueler作业调度的过程理解——作业正常执行结束 （执行结果及代码表现）： 

1. A job is finished by a child process, and a `exit()` is called.

   ```C
   if (execv(arglist[0],arglist) < 0)
   	printf("exec failed\n");
   		
   exit(1);
   ```

2. A `SIGCHLD` signal is raised and the customized handler `sig_handler()` is called

3. `sig_handler()` : query status and print out the corresponding message:

   ```C
   if (WIFEXITED(status)) {
   	current->job->state = DONE;
   	printf("normal termation, exit status = %d\tjid = %d, pid = %d\n\n",
   				WEXITSTATUS(status), current->job->jid, current->job->pid);
   }  else if (WIFSIGNALED(status)) {
   	printf("abnormal termation, signal number = %d\tjid = %d, pid = %d\n\n",
   	WTERMSIG(status), current->job->jid, current->job->pid);
   
   } else if (WIFSTOPPED(status)) {
   	printf("child stopped, signal number = %d\tjid = %d, pid = %d\n\n",
   	WSTOPSIG(status), current->job->jid, current->job->pid);
   }
   ```





#### Understand the process of job scheduling——job scheduling due to Priority(Execution results and corresponding code)：Schedueler作业调度的过程理解——因为优先级和进行作业调度（执行结果及代码表现）：

1. If the ready queue is not empty, check every job's information and select a job with highest priority. If a job's priority is equal to the highest priority, then check if its waiting time is larger, if so, select it.

   ```C
   for (prev = head, p = head; p != NULL; prev = p, p = p->next) {
   
   	if (p->job->curpri > highest || 
   				(p->job->curpri == highest && p->job->wait_time > select->job->wait_time)) {
   						
   		select = p;
   		selectprev = prev;
   		highest = p->job->curpri;
   	}
   }
   ```

2. Then assign the selected job to `next`

   ```C
   next = jobselect();
   ```

   

#### Understand the process of job scheduling——Job scheduling due to time slice (Execution results and corresponding code)：Schedueler作业调度的过程理解——因为时间片而进行作业调度（执行结果及代码表现）：

1. A timer is initialized with given time interval. It raises `SIGVTALRM` every period.

   ```C
   interval.tv_sec = 0;
   interval.tv_usec = 100;
   	
   new.it_interval = interval;
   new.it_value = interval;
   setitimer(ITIMER_VIRTUAL,&new,&old);
   ```

2. A customized handler is used to handle `SIGVTALRM`, which is `sig_handler()`:

   ```C
   newact.sa_sigaction = sig_handler;
   sigaction(SIGVTALRM,&newact,&oldact2);
   ```

3. If a `SIGVTALRM` is received, then `sig_handler()` will be called. And `schedule()` will be called after that:

   ```C
   void sig_handler(int sig, siginfo_t *info, void *notused)
   {
   	int status;
   	int ret;
   	
   	switch (sig) {
   	case SIGVTALRM:
   		schedule();
   		return;
   ......
   ```

4. Then everything is the same as explanations above this question.

