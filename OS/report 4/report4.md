1. Describe Function of `pthread_create`

Prototype:

```C
int pthread_create(pthread_t *thread, const pthread_attr_t *attr,void *(*start_routine) (void *), void *arg);
```

This function will create a new thread beginning from a specified subroutine (indicated by a function pointer and its arguments) according to the predefined attributes. This function will return 0 if no error occurs, otherwise, it will return the error state number.

Reference: http://man7.org/linux/man-pages/man3/pthread_create.3.html



2. Describe Function of `pthread_join`

Prototype: 

```C
int pthread_join(pthread_t thread, void **retval);
```

This function will block and wait for the termination of the specified thread and the status will be stored in retval. This function will return 0 if no error occurs, otherwise, it will return a error state number.

Reference: http://man7.org/linux/man-pages/man3/pthread_join.3.html



3. Describe Function of `pthread_mutex_lock`

Prototype: 

```C
int pthread_mutex_lock(pthread_mutex_t *mutex);
```

Lock the specified mutex object. If the mutex object is already locked, this function will block until the mutex object is available again. And return 0 if no error occurs, otherwise, an error number is returned.

The behavior varies according to the type of the mutex:

| Mutex                    | Description                                                 |
| ------------------------ | ----------------------------------------------------------- |
| PTHREAD_MUTEX_NORMAL     | deadlock is caused                                          |
| PTHREAD_MUTEX_ERRORCHECK | return error if the mutex is already locked                 |
| PTHREAD_MUTEX_RECURSIVE  | increase the lock count                                     |
| PTHREAD_MUTEX_DEFAULT    | result in undefined behavior if the mutex is already locked |

Reference: https://linux.die.net/man/3/pthread_mutex_lock



4. Describe Function of `pthread_cond_wait`

Prototype:

```C
int pthread_cond_wait(pthread_cond_t *restrict cond, pthread_mutex_t *restrict mutex);
```

This function will release mutex and block on a specified condition variable. And return 0 if no error occurs, otherwise, an error number is returned.

Note that before the calling process wakes up from this function, the calling process will acquire the mutex. So if someone signal the calling process waiting on some condition and the mutex is locked by other, then the calling process will wait for the mutex to unlock.

Reference:

https://linux.die.net/man/3/pthread_cond_wait

https://stackoverflow.com/questions/16522858/understanding-of-pthread-cond-wait-and-pthread-cond-signal/16524148



5. Describe Function of `pthread_cond_signal`

Prototype: 

```C
int pthread_cond_signal(pthread_cond_t *cond);
```

This function will "free" threads from waiting for the specified condition block. And return 0 if no error occurs, otherwise, an error number is returned. 

Using "free" instead of "Unblock" here is because the waiting threads now can acquire the mutex. But if it cannot acquire the mutex, the thread will still block.

Reference: 

https://linux.die.net/man/3/pthread_cond_wait

https://stackoverflow.com/questions/16522858/understanding-of-pthread-cond-wait-and-pthread-cond-signal/16524148



6. Describe Function of `pthread_mutext_unlock`

Prototype:

```C
int pthread_mutex_unlock(pthread_mutex_t *mutex);
```

This function will release a specified mutex. If there are many threads are blocking on this mutex, then after  the mutex is unblocked by this function, one of the thread will unblock.

The behavior varies according to the type of the mutex:

| Mutex                    | Description                                                 |
| ------------------------ | ----------------------------------------------------------- |
| PTHREAD_MUTEX_NORMAL     | result in undefined behavior if the mutex is NOT locked     |
| PTHREAD_MUTEX_ERRORCHECK | return error if the mutex is NOT locked                     |
| PTHREAD_MUTEX_RECURSIVE  | decrease the lock count                                     |
| PTHREAD_MUTEX_DEFAULT    | result in undefined behavior if the mutex is already locked |

Reference: https://linux.die.net/man/3/pthread_mutex_lock



7. Describe Function of `sem_open`

Prototype:

```C
sem_t *sem_open(const char *name, int oflag);
sem_t *sem_open(const char *name, int oflag, mode_t mode, unsigned int value);
```

This function will creates or open an existing semaphore specified by the name. `oflag`  specifies some operation:

| oflag             | description                                      |
| ----------------- | ------------------------------------------------ |
| O_CREAT           | Create a semaphore if it does not already exist. |
| O_CREAT \| O_EXCL | Return an error if the semaphore already exists. |

If `oflag` contains `O_CREAT`, two additional arguments MUST be supplied. `mode` specifies the permissions to be placed on the new semaphore. `value` is the initial value for the new semaphore.

Reference: http://man7.org/linux/man-pages/man3/sem_open.3.html



8. Describe Function of `sem_wait`

Prototype:

```C
int sem_wait(sem_t *sem);
```

If the value of the semaphore specified by `sem` is larger than 0, the value will be decreased and return immediately. If the value is 0, then this function will block until the value is larger than 0 again, and then proceed decrement and return.

Return 0 if no error occurs, otherwise, error number will be returned.

Reference: http://man7.org/linux/man-pages/man3/sem_wait.3.html



9. Describe Function of `sem_post`

Prototype:

```C
int sem_post(sem_t *sem);
```

The value of the semaphore specified by `sem` will be increased. 

Reference: http://man7.org/linux/man-pages/man3/sem_post.3.html



10. Describe Function of `sem_close`

Prototype:

```C
int sem_close(sem_t *sem);
```

Close the semaphore specified by `sem`. The resources allocated to the calling process for this semaphore can be freed.

Reference: http://man7.org/linux/man-pages/man3/sem_close.3.html



11. Producer-Consumer Problem（understand producer_consumer.c）: Are the data that consumers read from the buffer are produced by the same producer?

Yes.



12. Producer-Consumer Problem（understand producer_consumer.c）: What is the order of the consumer's read operations and the producer's write operations, and their relationship

If the queue is empty, the producer will write before the consumer read. If the queue is full, the consumer will read before the producer write. If the queue is not empty or full, the read and writer operation order is random, which means the read can go after another read or a write or a write can go after another write or read.



13. Producer-Consumer Problem（understand producer_consumer.c）: Briefly describe the result of the program

A visualized character picture is drawn to show the actual things happening in the producer, consumer and the ring queue delivering message from producer to consumer.

For example:

`[ ]<---| C | G | L | A | O |   |   |   |   |<---[O]`

This line means that producer is producing a new content `O`, and the ring queue still buffers five elements which are `C`, `G`, `L`, `A` and `O`. The consumer might be waiting for the producer to produce new content or sleeping.



14. Producer-Consumer Problem（understand producer_consumer.c）: What queue is used in this program, and its characteristics?

A ring queue is used in this program. It is a first-in-first out data structure.

Ring queue is implemented by an array whose size is fixed and consists a sequence of memory space. To fully utilize this array, two pointers are used to indicated the head of the queue and the tail of the queue. The new content might be appended to the front of the array while the element in front of it is placed at the end of the array. Thus, it is named as a ring queue.



15. Producer-Consumer Problem（understand producer_consumer.c）: Briefly describe the mutual exclusion mechanism of this program

Producer:

1. Acquire the mutex at first to block consumer to enter the critical section.

2. If the queue is full, then wait for the condition `full` and release the mutex to let the consumer consumer something to make some space. After consumer send signal and unlock the mutex, resume.

3. If the queue is empty, send signal to condition `empty`.

4. After produce a new element and put it to the queue, unlock the mutex.

Consumer:

1. Acquire the mutex at first to block producer to enter the critical section.
2. If the queue is empty, then wait for the condition `empty` and release the mutex to let the producer produce something to the queue. After producer send signal and unlock the mutex, resume.
3. If the queue is full, send signal to condition `full`.
4. After consume a element, unlock the mutex.