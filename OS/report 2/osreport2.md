**What is a system call:**

>The system call is the fundamental interface between an application and the Linux kernel.
>source: http://man7.org/linux/man-pages/man2/syscalls.2.html

In addition, when user try to require some special services, which is done by system call, the OS will switch to kernel mode and meet that requirements. The system call is used because of the security issue.



**What is fork:**

>fork() creates a new process by duplicating the calling process. The new process is referred to as the child process. The calling process is referred to as the parent process.
>source: http://man7.org/linux/man-pages/man2/fork.2.html

In addition, from the fork(), the child process and the parent process share the same memory content in their owned different address spaces. They also have the same code after fork(). But there are still some difference between child process created by fork() and its parent process:
1) The return values of fork is different in parent process and child process.
2) The process id, a.k.a. pid.
3) The running time of the child process is reset to zero.
4) The file locks



**How to realize inter-process communication:**

There are several ways to realize it:

1) `shared memory`. Two processes both can read and write the same piece of memory. They can exchange messages to each other on it.

2) `pipe`, a data channel, the details are shown in the next question

3) `message queue` and `mailbox`. 

4) `semaphore`



**How to realize inter-process connection:**

Breif idea: Using `pipe`, which is a data channel. 
Since `pipe` is a unidirectional data channel, if two processes suppose to talk to each other, two pipes are used. For short, the following description shows how to realize inter-process communication in one direction.
1) call `int pipe(int pipefd[2]);`, where pipefd are two file descriptors. One for read end, another one for write end.
2) create a char buffers for read and write.
3) At the read end, call `read(pipe_fd[0], <address of the buffer>, <size of the buffer>);` to read data from the other side in blocked way.
4) At the write end, call `write(pipe_fd[1], <address of the buffer>, <size of the message>);`, to write data into the pipe.
5) Call `close(pipe_fd[<0/1>]);` to close an end if that end is unused.

> Reference: code for report.zip



**Write the prototype of function "fork":**

```C
/* prototype */ pid_t fork(void);
```

> Reference: http://man7.org/linux/man-pages/man2/fork.2.html



**Write the prototype of function "signal":**

```C
typedef void (*sighandler_t)(int);
/* prototype */ sighandler_t signal(int signum, sinhandler_t handler);
```

> Reference: http://man7.org/linux/man-pages/man2/signal.2.html





**Write the prototype of function "pipe":**

```C
/* On Alpha, IA-64, MPIS, SuperH, and SPARC/SPARC64 */
struct fd_pair{
  long fd[2];  
};
/* prototype */ struct fd_pair pipe();
/* on all other architectures */
/* prototype */ int pipe(int pipefd[2]);
int pipe2(int pipefd[2], int flags)
```

> Reference: http://man7.org/linux/man-pages/man2/pipe.2.html





**Write the prototype of function "tcsetpgrp":**

```C
/* prototype */ pid_t tcgetpgrp(int fd);
```





**Execute "fork.c" and observe, please describe the result (not execution result)：**

There is no other information printed except for the result of `ls`.  The contents of the `printf()` are not shown because they are in the buffer. If `fflush(stdout)` is added after it, the result can be shown on the screen. Appending `\n` at the end of the sentence to be printed also works.

After fixing this "bug",  we can see that the parent process print `parent exists` only when the result of `ls` is printed on the screen. This is because of the `waitpid()` function. Only when the child process is terminated, this function stops to block the process.



**Execute "fork.c" and observe, please describe how to distinguish between parent and child processes in a program：**

The return value of `fork()` is different in child process and parent process. In the child process, the return value is 0, while in parent process this value is the process id of the child process. Simply checking the return value can distinguish between them.



**Execute "pipe.c" and observe, please describe the result (not execution result)：**
![](http://q5o7o1h4r.bkt.clouddn.com/Fq-k70GnmmZuFVyubS8dgNX8POeF)
The message in the `rwBuffer` should be shown in the screen at first, since process `pid[0]` is blocked. Furthermore, process `pid[1]` yield no output because of that. 
After showing the communication message between process `pid[0]` and parent process, the content of `ls` is shown. If the length of the content is more than one page, a `more` label is shown on the left corner. 



**Execute "pipe.c" and observe.  Is execvp(prog2_argv[0],prog2_argv)(Line 56) executed? And why? :**
As shown in the last picture, `pipe[1]` is closed and copied to stdout, the content of `ls` cannot be printed directly on the screen. Since the content of `ls` is shown, it must be shown via `must`, or say the process `pid[1]`. Thus, `more` works.



**Execute "signal.c" and observe, please describe the result (not execution result)：**

If there is no more operations after calling the `main()` function, the program should keep printing `PID(parent): <process id of the parent process>\nPID(child): <process id of the child process>`. The order of the printed information from different process may be different at each iteration, since the scheduler can put anyone of them to execution at first.

If `ChildHandler()` is triggered, the program first print `The process generating the signal is PID:...`

Then, if one of the child process of this process (process who triggers the handler) is out, then `The child is gone!!!!!` is printed. 

If there is no child out, `Uninteresting` is printed. This can be realized by sending `SIGCHLD` to the child process. Or, using `kill` to directly send `SIGCHLD` to the parent process.



**Execute "signal.c" and observe. Please answer, how to execute function ChildHandler? :** 

Since in `sigaction(SIGCHLD,&action,NULL);` , `action`, to which `ChildHandler` is binded, is assigned to signal `SIGCHLD`. Thus, send signal `SIGCHLD` to either child process or parent process, this function will be executed.

Sending `SIGCHLD` to a process can be done by `kill -17 <child process id / parent process id>`. The child process of this process exits by itself will also send `SIGCHLD` to this process.



**Execute "process.c" and observe, please describe the result (not execution result)：**

A running`vi` program is shown at first. After shutting it down, `ID(child)=?` and `ID(parent)=?` both are printed on the screen, the printing order is depended on the scheduler. Then, an echo process shows up.



**Execute "process.c" and observe. Please answer, how many ./process in the process list? And what’s the difference between them?:**

Two ./process are in the process list. One of them is another one's child process. Between parent process and its child process, there are many differences, such as, the address spaces, process id,  running time.

In details, the parent process is an echo program, as shown in the picture below. And child process is a running `vi` program.
![](http://q5o7o1h4r.bkt.clouddn.com/FluUp7ueJDTmZ8-IitI8y7cCqdY4)



**Execute "process.c" and observe. Please answer, what happens after killing the main process:**
The running `vi` program shuts down immediately. And the unprinted message in the code shows up. And some error messages from Vim also print on the screen. The picture below can tell this scene.
![](http://q5o7o1h4r.bkt.clouddn.com/FqvnBiSXeVxHPafeMf-3jf8JmqhD)



**Make a conclusion here：**

Read more docs. Get some sleeps.