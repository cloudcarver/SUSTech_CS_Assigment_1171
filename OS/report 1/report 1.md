## Question 1 ~ 13

#### 1

**run"mkdir ~/studentID" （replacing studentID with your own ID）**

**Answer the function and parameter meaning:**

`mkdir` means make a new directory. The parameter indicates the place to make a new directory. Parameter `~/studentID` means create a directory named `studentID` in the home path which indicated by `~`.

![](http://q5o7o1h4r.bkt.clouddn.com/FjkZwUy3ZJQKlOpqdSeCmiGBHDcK)



#### 2

**run"ls –la ~ " （replacing studentID with your own ID）** 

**Answer the function and parameter meaning:**

`ls` means list. `ls` command list information about the files.`a` mens all (all entries including those starting with a dot `.`). And `l` means using a long listing format.

![](http://q5o7o1h4r.bkt.clouddn.com/FgMTLGZYm5pjXc9ST1YzhQt9wLaR)



#### 3

**run" cd ~/studentID " （replacing studentID with your own ID）** 
**Answer the function and parameter meaning:**

`cd` is used to open an directory or go to that directory. The parameter means the directory you want to go. `~/studentID` means a directory named studentID in home path which is indicated by `~`.

![](http://q5o7o1h4r.bkt.clouddn.com/FhwzFhZ1XzeTdx3J101LnXskIs6J)



#### 4

**run" man grep" （replacing studentID with your own ID）** 
**Answer the function and parameter meaning:**

`man` means manual. The parameter is the name of the application which you need a manual of it and know the details like usage, parameters of this application. `grep` is an application searching for pattern to each file. If no file is found, search recursively.

![](http://q5o7o1h4r.bkt.clouddn.com/Fqq58yWcgGAQxY2O5bUeIVvkZ47D)



#### 5

**run" mv ~/studentID /home "and" ls /home " （replacing studentID with your own ID）** 
**Answer the function and parameter meaning:** 

`mv` means move files or rename files. The first parameter is the source file, which is `~/studentID` and the second parameter is the destination file, which is `home`.

![](http://q5o7o1h4r.bkt.clouddn.com/FsQ95mNKQI6HI19314ilSca4Ei2O)



#### 6

**run" rm -r /home/studentID  "（replacing studentID with your own ID）**

**Answer the function and parameter meaning:** 

`rm` means remove. To remove a directory, option `r` is used, which means `recursively`, which indicates that all the files under this directory will be removed as well. The parameter is the path of the file to be removed. 

![](http://q5o7o1h4r.bkt.clouddn.com/FpxroapnL7bwDmBGlra9vjdL4w49)



#### 7

**run"  cp /etc/apt/sources.list /etc/apt/sources.list.bak  "（replacing studentID with your own ID）**

**Answer the function and parameter meaning:** 

`cp` means copy. The first parameter is the source file. The seconda parameter is the destination file. 

![](http://q5o7o1h4r.bkt.clouddn.com/Fi1OxPKCJtnn30Nq8xLNoe_iqI9i)



#### 8

**run" cat /etc/shells "（replacing studentID with your own ID）
Answer the function and parameter meaning:** 

cat is used to concatenate files and print on the standard output. In other word, it can read the given file and then output them to the standard output. The parameter is the file. 

![](http://q5o7o1h4r.bkt.clouddn.com/FqfFoV7WOtVL2KTKummFLc0GZqp9)



#### 9

**run" cat /etc/shells | grep bash "（replacing studentID with your own ID）
Answer the function and parameter meaning:** 

SInce `grep` is used to find pattern. `|` is a tunnel, which can be explained as a filter or "post-processor". ` | grep bash` means output lines matching the given pattern in standard output, which is indicated by `cat`.

![](http://q5o7o1h4r.bkt.clouddn.com/Fgu6aNdEbdK31V9Oj-W-TO3AU2l2)



#### 10

**Open two terminals, find their PIDs by ps and kill one of them**

**Answer the function and parameter meaning:** 

ps means reporting a snapshot of the current processes. `kill` is used to send a signal to a given process. `kill -kill <pid> ` means kill this process

![](http://q5o7o1h4r.bkt.clouddn.com/FmafIJBoHfOavmG-sxTRxo6eqVrK)



## Question 11

### Source Code

```c
#include <stdio.h>
int main(){
    int x = 0;
    x += 1;
    x += 1;
    x += 1;
    printf("%d\n", x);
    return 0;
}
```



### Two different ways to optimize the code

First, use parameter `-O0` to compile and optimize the code

```c
gcc -S opt.c -O0 -o opt0.s
```

The assembly code looks like:

![](http://q5o7o1h4r.bkt.clouddn.com/FtN7ZDxyi1pdaZeEDlfaAmH3qBJa)

We can see that `addl $1, -4(%rbp)` is run three times. To increase a value for three times like the source code in C suggests:

```c
...

    int x = 0
    x += 1
    x += 1
    x += 1
...

```



Then, use parameter `-O1` to do the compile and optimization.

The assembly code look like:

![](http://q5o7o1h4r.bkt.clouddn.com/Fm28j6XKqXmoeC11IjVc32eEe1sF)

And no more redundant code here since 3 is directly move to the register `%edx` in `movl $3, %edx`.



### Conclusion

In short, the second method is way more clean than the first one. Because the second assembly code has less lines of code than the first one, it gains better performance.

`EOF`