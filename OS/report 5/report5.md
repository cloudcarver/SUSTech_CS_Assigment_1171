What is deadlock?

Deadlock is a phenomenon causes starvation when circular waiting for resources between threads occurs. Thus, it occur with multiple resources. Deadlock is not always deterministic which means it will not always happen in a piece of code that might potentially cause deadlock.



What are the requirements of deadlock?

1. Mutual exclusion: only one thread at a time can use a resource

2. Hold and wait: thread holding at least one resource is waiting to acquire additional resources held by other threads

3. No preemption: resources are released only voluntarily by the thread holding the resource, after thread is finished with it

4. Circular wait: there exists n waiting threads, $T_i$ is waiting for a resource that is held by $T_{(i\ \mathrm{mod} \ n)+1 }$



What's the difference between deadlock prevention and deadlock avoidance?

- Deadlock prevention makes sure that if there will be a deadlock when the job is running, prevent it from happening. It ensure that at least one of the four requirements for deadlock can never occur.

- Deadlock avoidance makes sure that once the job starts, there will be no deadlock in progress. It ensure that once a request is granted, it is safe, which means at least one of the necessary requirements for deadlock cannot occur. It requires that the OS be given additional information in advance concerning which resources a process will request and use during its lifetime.



How to prevent deadlock? Give at least two examples.

1. Do not allow waiting. On collision, back off and retry.
2. Make all threads requests everything they will need at the beginning.
3. Force all threads to request resources in a particular order preventing any cyclic use of resources.



Which way does recent UNIX OS choose to deal with deadlock problem, why?

Ignore the problem and pretend that deadlocks never occur in the system.

Deadlock detection and prevention consume a lot of resources. Ignoring the possibility of deadlocks is cheaper than the other approaches. In UNIX OS, deadlock occur infrequently, the extra expense of the other methods may not seem worthwhile. 



What data structures you use in your implementation (of Banker's algorithm) ? Where and why you use them? Are they optional for your purpose?



1. A struct to keep tracking the state of a process:

```C++
struct process{
    std::vector<int> allocated;
    std::vector<int> max;
    ......
};
```

Used in everywhere.

This is optional. Since we can use separate vector to keep tracking the `allocated` and `max` state for every process. This is for making the code readable and easier to maintain.



2. An unordered map to keep tracking the state of all running(not terminated yet) processes in the system.

```C++
std::unordered_map<int, process> processes_map;
```

This is a state variable of the system. Used in determine the system is safe or not and used when need to update the state, e.g., terminate a process, insert a new process, etc.

This is not optional. Because the number of processes is dynamic, a dynamic container is needed. And we also need to get a process via the process id. Thus, a map is necessary. 



3. A vector to store the total number of all resources.

```C++
std::vector<int> rscTyps;
```

Used when need to check the total number of all resources.

This is optional since we don't need to know the total number of all resources at any time. It is for debug usage.



4. A vector to keep tracking the current available resources.

```c++
std::vector<int> avaliable;
```

This is a state variable of the system. Used in determine the system is safe or not and used when need to update the state, e.g., terminate a process, insert a new process, etc.

This is not optional. Since we need to keep tracking the available resources and the number of resources is varies in different test cases. Thus a vector is needed for these purposes.



