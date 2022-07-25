#include <bits/stdc++.h>
#include <unistd.h>

using namespace std;

#define PROCESS_NAME_LEN 32 //进程名最大长度
#define MIN_SLICE 10 //内碎片最大大小
#define DEFAULT_MEM_SIZE 1024  //总内存大小
#define DEFAULT_MEM_START 0  //内存开始分配时的起始地址
#define BEST_FIT 1
#define WORST_FIT 2
#define FIRST_FIT 3
#define BUDDY_SYSTEM 4
#define DEFAULT_ALGORITHM 3

int mem_size = DEFAULT_MEM_SIZE;
bool flag = 0; //当内存以及被分配了之后，不允许更改总内存大小的flag
static int pid = 0;

int algorithm = DEFAULT_ALGORITHM;

struct free_block{	//空闲数据块
	int size;
	int start_addr;
	struct free_block *next;
};

struct allocated_block{ //已分配的数据块
	int pid;
	int size;
	int start_addr;
	int *data;
	struct allocated_block *next;
};

free_block *free_block_head; //空闲数据块首指针
allocated_block *allocated_block_head = NULL; //分配块首指针

allocated_block *find_process(int id); //寻找pid为id的分配块
free_block *init_free_block(int mem_size); //空闲块初始化
void display_menu(); //显示选项菜单
void set_mem_size(); //设置内存大小
int allocate_mem(int mem_sz, allocated_block *ab); //为制定块分配内存
void rearrange(); // 对块进行重新分配
int create_new_process(); //创建新的进程
int free_mem(allocated_block *ab); //释放分配块
void swap(int *p, int *q); //交换地址
int dispose(allocated_block *ab); //释放分配块结构体
void display_mem_usage(); //显示内存情况
void kill_process(); //杀死对应进程并释放其空间与结构体
void Usemy_algo(int id); //使用对应的分配算法

/**
 * Call Hieraechy
 * 
 * set_mem_size()
 * create_new_process() -> allocate_mem()
 * kill_process() -> find_process() -> free_mem() -> dispose()
 * display_mem_usage()
 * 
 * unused:
 * rearrange() -> swap()
*/

//主函数
int main(){
	int op;
	pid = 0;
	free_block_head = init_free_block(mem_size); //初始化一个可以使用的内存块，类似与操作系统可用的总存储空间
	for(;;){
		// sleep(1);
		display_menu();
		fflush(stdin);
		scanf("%d", &op);
		switch (op){
			case 1:{ set_mem_size(); break; }
			case 2:{
				int alg;
				printf("Choose an algorithm\n");
				printf("1: Best Fit\n 2: Worst Fit\n 3: First Fit\n 4: Buddy System\n");
				scanf("%d", &alg);
				Usemy_algo(alg);
				break;
			}
			case 3:{ create_new_process(); break; }
			case 4:{ kill_process(); break; }
			case 5:{ display_mem_usage(); break; }
			case 233:{ puts("bye...."); sleep(1); return 0; }
			defaut: break;
		}
	}
}

/**
 * Return the corresponding allocated block.
 * Return NULL if pid not found.  
*/
allocated_block *find_process(int id){ //循环遍历分配块链表，寻找pid=id的进程所对应的块

	allocated_block *p;
	for(p = allocated_block_head; p != NULL; p = p->next)
		if(p->pid == id)
			return p;
	
	return NULL;
}

free_block *init_free_block(int mem_size){ //初始化空闲块，这里的mem_size表示允许的最大虚拟内存大小
	free_block *p;
	p = (free_block *)malloc(sizeof(free_block));
	if (p == NULL){
		puts("No memory left");
		return NULL;
	}
	p->size = mem_size;
	p->start_addr = DEFAULT_MEM_START; 
	p->next = NULL;
	return p;
}

void display_menu(){
	puts("\n\n******************menu*******************");
	printf("1) Set memory size (default = %d)\n", DEFAULT_MEM_SIZE);
	printf("2) Set memory allocation algorithm (default = %s)\n", "first fit");
	printf("3) Create a new process\n");
	printf("4) Kill a process\n");
	printf("5) Display memory usage\n");
	printf("233) Exit\n");
}

void set_mem_size(){ //更改最大内存大小
	if(flag != 0){
		printf("Cannot change the memory size. There should be no allocated memory when changing memory size.\n");
	}else{
		printf("Please input new memory size:\n");
    	scanf("%d", &mem_size);
		free_block_head->size = mem_size;
	}
}

int allocate_mem(int mem_sz, allocated_block *ab){ //为块分配内存，真正的操作系统会在这里进行置换等操作
	free_block *p, *pre;
	if(algorithm == FIRST_FIT){
		for(p = free_block_head, pre = free_block_head; p != NULL; pre = p, p = p->next)
			if(p->size >= mem_sz)
				break; 
	}else if(algorithm == BEST_FIT){
		free_block *best = NULL, *best_pre = NULL;
		int minimum_gap = mem_size;
		for(p = free_block_head, pre = free_block_head; p != NULL; pre = p, p = p->next){
			if(p->size >= mem_sz && p->size - mem_sz < minimum_gap){
				minimum_gap = p->size - mem_sz;
				best_pre = pre;
				best  = p;
			}
		}
		p = best;
		pre = best_pre;
	}else if(algorithm == WORST_FIT){
		free_block *worst = NULL, *worst_pre = NULL;
		int maximum_gap = -1;
		for(p = free_block_head, pre = free_block_head; p != NULL; pre = p, p = p->next){
			if(p->size >= mem_sz && p->size - mem_sz > maximum_gap){
				maximum_gap = p->size - mem_sz;
				worst_pre = pre;
				worst  = p;
			}
		}
		p = worst;
		pre = worst_pre;
	}else{ /* algorithm == BUDDY_SYSTEM */
		for(p = free_block_head, pre = free_block_head; p != NULL; pre = p, p = p->next){
			if(p->size >= mem_sz){
				while(p->size >= 2 * mem_sz){
					free_block *newblock = (free_block*)malloc(sizeof(free_block));
					newblock->size = p->size / 2;
					p->size -= newblock->size;
					newblock->start_addr = p->start_addr + p->size;
					newblock->next = p->next;
					p->next = newblock;
				}
				break;
			}
		}
	}
	
	/* Not enough space */
	if((p == NULL && pre != NULL) || pre == NULL)
		return -1;
	
	flag = 1;
	/* Allocate new space */
	ab = (allocated_block*)malloc(sizeof(allocated_block));
	ab->pid = ++pid;
	ab->start_addr = p->start_addr;
	if(algorithm == BUDDY_SYSTEM){
		ab->size = p->size;
	}else{
		ab->size = mem_sz;
	}
	
	ab->data = (int*)malloc(ab->size);

	/* Deal with free chain */
	if(ab->size != p->size){
		p->size -= mem_sz;
		p->start_addr += mem_sz;
	}else{
		if(p == pre){
			free_block_head = p->next;
			free(p);
		}else{
			pre->next = p->next;
			free(p);
		}
	}

	/* Deal with allocated chain */
	allocated_block *abp, *abpre;
	for(abp = allocated_block_head, abpre = allocated_block_head; abp != NULL; abpre = abp, abp = abp->next)
		if(abp->start_addr > ab->start_addr)
			break;
	if(abpre == NULL){ /* empty list */
		allocated_block_head = ab;
	}else{
		if(abp == abpre){ /* Should be the head */
			ab->next = abp;
			allocated_block_head = ab;
		}else{ /* Should be placed in the middle or tail */
			abpre->next = ab;
			ab->next = abp;
		}
	}
}

int create_new_process(){ //创建新进程
	int mem_sz = 0;
	printf("Please input memory size\n");
    scanf("%d", &mem_sz);
    // Write your code here
	int rtn;
	if(0 < algorithm && algorithm < 5){
		allocated_block *p = NULL;
		rtn = allocate_mem(mem_sz, p);
		if(rtn == -1){
			printf("Failed to create new process: Not enough memory.\n");
		}
	}else{
		printf("Failed to create new process: No such algorithm.\n");
		return -1;
	}
}

void swap(int *p, int *q){
	int tmp = *p;
	*p = *q;
	*q = tmp;
	return;
}

void rearrange(){ //将块按照地址大小进行排序
	free_block *tmp, *tmpx;
	puts("Rearrange begins...");
	puts("Rearrange by address...");
	tmp = free_block_head;
	while(tmp != NULL){
		tmpx = tmp->next;
		while (tmpx != NULL){
			if (tmpx->start_addr < tmp->start_addr){
				swap(&tmp->start_addr, &tmpx->start_addr);
				swap(&tmp->size, &tmpx->size);
			}
			tmpx = tmpx->next;
		}
		tmp = tmp->next;
	}
	usleep(500);
	puts("Rearrange Done.");
}

int free_mem(allocated_block *ab){ //释放某一块的内存
	free(ab->data);
	printf("allocated ab's start_addr: %d\n", ab->start_addr);
	printf("allocated ab's size: %d\n", ab->size);
	
	free_block *p, *pre, *newblock;
	for(p = free_block_head, pre = free_block_head; p != NULL; pre = p, p = p->next){
		if(p->start_addr > ab->start_addr){

			if(p != pre){ /* There is a block in front of newblock, and a block behind newblock */
				if(pre->start_addr + pre->size == ab->start_addr){ /* Pre and newblock can merge */
					pre->size += ab->size;
					newblock = pre;
				}else{ /* Pre and newblock CANNOT merge */
					newblock = (free_block*)malloc(sizeof(free_block));
					newblock->size = ab->size;
					newblock->start_addr = ab->start_addr;
					newblock->next = pre->next;
					pre->next = newblock;
				}
			}else{ /* The new block should be the head */
				printf("head\n");
				newblock = (free_block*)malloc(sizeof(free_block));
				newblock->start_addr = ab->start_addr;
				newblock->size = ab->size;
				newblock->next = p;
				free_block_head = newblock;
			}
			
			if(algorithm == BUDDY_SYSTEM){ /* Merge buddy */
				free_block *b = free_block_head;
				free_block *merged_buddy;
				while(b!= NULL && b->next != NULL){
					if(b->start_addr + b->size == b->next->start_addr && b->size == b->next->size){
						merged_buddy = b->next;
						b->size += merged_buddy->size;
						b->next = merged_buddy->next;
						free(merged_buddy);
					}else{
						b = b->next->next;
					}
				}
			}else{
				/* See if the newblock and p can merge  */
				if(ab->start_addr + ab->size == p->start_addr){ /*[new + p] = [new]*/
					newblock->size += p->size;
					newblock->next = p->next;
					free(p);
				}
			}
			

			return 0; /* Job done, return */
		}
	}

	/* cannot find a suitable place in list */
	newblock = (free_block*)malloc(sizeof(free_block));
	newblock->size = ab->size;
	newblock->start_addr = ab->start_addr;
	newblock->next = NULL;
	if(pre == NULL){ /* The list is empty */
		free_block_head = newblock;
	}else{ /* should be at the end of the list. */
		pre->next = newblock;
	}
}

int dispose(allocated_block *fab){ //释放结构体所占的内存
	allocated_block *pre, *ab;
	if (fab == allocated_block_head){
		allocated_block_head = allocated_block_head->next;
		free(fab);
		return 1;
	}
	pre = allocated_block_head;
	ab = allocated_block_head->next;
	while (ab != fab){ pre = ab; ab = ab->next;}
	pre->next = ab->next;
	free(ab);
	return 2;
}

void display_mem_usage(){
	free_block *fb = free_block_head;
	allocated_block *ab = allocated_block_head;
	puts("*********************Free Memory*********************");
	printf("%20s %20s\n", "start_addr", "size");
	int cnt = 0;
	while (fb != NULL){
		cnt++;
		printf("%20d %20d\n", fb->start_addr, fb->size);
		fb = fb->next;
	}
	if (!cnt) puts("No Free Memory");
	else printf("Totaly %d free blocks\n", cnt);
	puts("");
	puts("*******************Used Memory*********************");
	printf("%10s %10s %20s\n", "PID", "start_addr", "size");
	cnt = 0;
	while (ab != NULL){
		cnt++;
		printf("%10d %10d %20d\n", ab->pid, ab->start_addr, ab->size);
		ab = ab->next;
	}
	if (!cnt) puts("No allocated block");
	else printf("Totally %d allocated blocks\n", cnt);
	return;
}

void kill_process(){ //杀死某个进程
	allocated_block *ab;
	int pid;
	puts("Please input the pid of Killed process");
	scanf("%d", &pid);
	ab = find_process(pid);
	if (ab != NULL){
		free_mem(ab);
		dispose(ab);
	}
}

void Usemy_algo(int alg){
	if(alg < 1 && 4 < alg){
		printf("No such algorithm. Use best fit.");
		algorithm = BEST_FIT;
	}else if(alg == 4 && (free_block_head == NULL || free_block_head->size != mem_size)){
		printf("Can only switch to buddy system when the memory is NOT allocated yet. Use best fit.");
		algorithm = BEST_FIT;
	}else{
		algorithm = alg;
		switch(algorithm){
			case 1:{printf("Use best fit.\n"); break;}
			case 2:{printf("Use worst fit.\n"); break;}
			case 3:{printf("Use first fit.\n"); break;}
			case 4:{printf("Use buddy system.\n"); break;}
			default:{printf("Usemy_algo: Error."); exit(-1);}
		}
	}
}