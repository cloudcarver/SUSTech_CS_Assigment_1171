#include"init.h"

void *reader(int *buffer){

    /* Wait for the file to be free */
    sem_wait(&rc);
    if(readcount++ == 0){ // first reader lock the door (this door can only block writer)
        sem_wait(&db);
    }
    sem_post(&rc);

    printf("Reader gets sem\n");

    /* Read a thing */
    char *path = "BUFFER.TXT";
    int fd = open(path, O_RDONLY);
    read(fd, buffer, 4);
    printf("Reader reads %d and releases\n", *buffer); 
    close(fd);

    /* Free the file */
    sem_wait(&rc);
    if(--readcount == 0) // last reader open the door
        sem_post(&db);
    sem_post(&rc);
    
}

