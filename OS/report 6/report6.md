What is Uniprogramming: What is the shortcoming of Uniprogramming:

In uniprogramming, application always runs at same place in physical memory since only one application at a time. Application can access any physical address.  Thus, uniprogramming is not powerful since it allows only one application running at a time. And it is also not efficient since switching application on it will be really time consuming.



What is Multiprogramming: What is the shortcoming of Multiprogramming:

In multiprogramming, multiple programs can run at a time by using two special registers BaseAddr and LimitAddr to prevent user from straying outside designated area. Thus, multiprogramming need to consider fragmentation problem for managing the memory. If the strategy is not good, some available memory may be wasted. And some good strategy may cost a lot of resources.



What is the segmentation mechanism and its advantages & disadvantages:

Segmentation is a memory-management scheme that supports a logical address space view by using a segment table which maps the logical address to a physical address. 

Advantages: 

1. It logically manages the data, thus it is easy to share and protection. 
2. It also reduces fragmentation.  
3. Segmentation efficient for sparse address spaces

Disadvantages: 

1. Segment size is not fixed, this make it more complicated. 
2. One process need allocate memory many times. 
3. Fragmentation is smaller but still a problem.
4. May move processes multiple times to fit everything
5. Limited options for swapping to disk



What is the paging mechanism and its advantages & disadvantages:

Paging is a memory-management scheme that permits the physical address space of a process to be non-contiguous and also avoids external fragmentation and the need of compaction. It breaks physical memory into fixed-sized blocks called frames and breaks logical memory into blocks of the same size called pages. It uses a page table to maps logical addresses to physical addresses.

Advantages:

1. Simple to implement
2. Avoid external fragmentation

Disadvantages:

1. Page table requires extra memory space
2. Internal fragmentation problem





How to reduce the occurrence of internal fragmentation when allocating memory? Briefly explain why this method works.

Use best fit, first fit or worst fit algorithm. Because in these algorithm, the free block will be split into two parts. One of these two parts will be the same size as the required size. But the used memory should be known before. In this case, there is no internal fragmentation since we know exactly how many bytes are needed.

If this information is unknown, then use paging with small page size. The internal fragmentation will be reduced if page size is reduced. If page size is 1 byte, then there is no internal fragmentation.



How to reduce the occurrence of external fragmentation when allocating memory? Briefly explain why this method works.

Compaction. Reschedule the allocated plan to make the separated external fragment a single continuous memory space again. Why? The external fragments with small size has little chance to be allocated to processes. So they can be merged by shuffling the fragments and become a one single big memory space.

Segment and paging. Use virtual memory to map some separated fragments to one single continuous memory space. Thus, make the small piece useful again just like compaction but with much better performance.

