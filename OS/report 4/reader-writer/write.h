#include"init.h"

void *writer(int *buffer){

    /* Wait for the file to be free */
    sem_wait(&db);
    printf("writer gets sem\n");
    
    /* Write a thing */
    char *path = "BUFFER.TXT";
    int fd = open(path, O_WRONLY);
    (*buffer)++;
    write(fd, buffer, 4);
    close(fd);
    printf("writer writes %d and releases\n", *buffer);

    /* Free the file */
    sem_post(&db);
}

