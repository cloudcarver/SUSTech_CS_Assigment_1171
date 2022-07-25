#include"init.h"
#include"read.h"
#include "write.h"
pthread_t rehs[600], wrhs[25];
sem_t db,rc;
int readcount;
int main(){
	int nw,nr;
    printf("\nEnter the no readers : ");
    scanf("%d",&nr);
    printf("\nEnter the no Writers : ");
    scanf("%d",&nw);
	sem_init(&db, 0, 1);
	sem_init(&rc, 0, 1);
    readcount = 0;
	int buffer = 0;
	int i = 0, j =0, k = 0, r = 0;

	srand(time(0));
	
	pthread_create(&rehs[k++],NULL,reader,&buffer);
	sleep(1);

	pthread_create(&wrhs[j++],NULL,writer,&buffer);
	sleep(1);
	pthread_create(&rehs[k++],NULL,reader,&buffer);
	pthread_create(&wrhs[j++],NULL,writer,&buffer);
	pthread_create(&rehs[k++],NULL,reader,&buffer);
	pthread_create(&wrhs[j++],NULL,writer,&buffer);
	pthread_create(&rehs[k++],NULL,reader,&buffer);
	sleep(5);
	pthread_create(&wrhs[j++],NULL,writer,&buffer);
	pthread_create(&wrhs[j++],NULL,writer,&buffer);
	sleep(5);
	pthread_create(&wrhs[j++],NULL,writer,&buffer);
	pthread_create(&rehs[k++],NULL,reader,&buffer);
	pthread_create(&rehs[k++],NULL,reader,&buffer);
	pthread_create(&rehs[k++],NULL,reader,&buffer);
	


    for (i = 0; i < j; i++)
		pthread_join (wrhs[i], NULL);
	for (i = 0; i < k; i++)
		pthread_join (rehs[i], NULL);
}
