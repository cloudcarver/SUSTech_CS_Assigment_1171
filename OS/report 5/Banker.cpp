#include <iostream>
#include <iomanip>
#include <string.h>
#include <unordered_map>
#include <vector>

/*=========================== Assignment: Banker's Algorithm ===============================

Date: 2020/4/13
Author: 11710403

===================================== Inpute & Ouput ======================================= 
Input: 
First line is an integer r, which is the number of resource types.
The second line will be r integers, which are the maximum quantity of each resource
Then will be following a list of commands. The commands are in three form
    1. New process registering, such as "1678 new 6 5 0 7", means process 1678 
       is a new process, whose maximum need of each resource is 6 5 0 7 (assume r is 4) 
    2. Resource requesting, such as "233 request 0 4 5 3", means process 233 is an old 
       process, it request more resource, the need of each resource is 0 4 5 3.
    3. Process termination, such as "233 terminate", means process 233 terminate and 
       return all resources it holding.
Output:
For each command, output "OK", or "NOT OK" to determine if the command can execute. 
If OK, execute the command.
===========================================================================================*/

// #define BANKER_DEBUG

#ifdef BANKER_DEBUG
#include <fstream>
#endif

struct process{
    std::vector<int> allocated;
    std::vector<int> max;
    process(std::vector<int> *_max){
        max.assign(_max->begin(), _max->end());
        allocated.insert(allocated.begin(), max.size(), 0);
    }
};

void debugMap(std::unordered_map<int, process>* processes_map, int numRscTyp, std::vector<int>* rscTyps, std::vector<int>* avaliable){

    std::cout << "    Total  ";
    for(int val : *rscTyps){
        std::cout << std::setw(3) << val;
    }
    std::cout << std::endl;

    std::cout << "Available  " ;
    for(int val : *avaliable){
        std::cout << std::setw(3) << val;
    }
    std::cout << std::endl << std::endl;

    std::cout << std::setw(10) << "Process" << std::setw(3 * numRscTyp) << "max" << "    " << std::setw(3 * numRscTyp) << "allocated" << std::endl;

    for(int i = 0; i < numRscTyp * 6 + 14; i++)
        std::cout << "-";
    std::cout << std::endl;

    for(auto& itr : *processes_map){
        std::cout << std::setw(3 * numRscTyp) << itr.first;
        process p = itr.second;
        std::vector<int> max = p.max;
        std::vector<int> allocated = p.allocated;
        
        for(int i = 0; i < max.size(); ++i){
            std::cout << std::setw(3) << max[i];
        }

        std::cout << "    ";

        for(int i = 0; i < allocated.size(); ++i){
            std::cout << std::setw(3) << allocated[i];
        }
        std::cout << std::endl;
    }
}

bool isRscSmallerOrEqual(std::vector<int>* rsc1, std::vector<int>* rsc2){
    if(rsc1->size() != rsc2->size()){
        std::cout << "isRscSmallerOrEqual: Two resources arrays should have the same size." << std::endl;
        exit(-1);
    }

    for(int i = 0; i < rsc1->size(); ++i){
        if((*rsc1)[i] > (*rsc2)[i])
            return false;
    }
    
    return true;
}

/* Determine that current state is safe or not */
bool safeChecking(std::unordered_map<int, process>* processes_map, std::vector<int>* avaliableRsc){

    /* Copy the state of the system to see whether a safe sequence exists or not */
    std::unordered_map<int, process> processes_map_tmp(*processes_map);
    std::vector<int> avaliable(*avaliableRsc);

    std::vector<int> deleteIndices; // the indices of the processes need to be deleted (finished). 
    bool notDone = true;

    do{
        deleteIndices.clear();
        notDone = false;
        
        for(auto& itr : processes_map_tmp){
            std::vector<int> request(itr.second.max.size(), 0);
            
            for(int i = 0; i < request.size(); ++i)
                request[i] = itr.second.max[i] - itr.second.allocated[i];
            
            if(isRscSmallerOrEqual(&request, &avaliable)){
                deleteIndices.push_back(itr.first);
                for(int i = 0; i < avaliable.size(); ++i)
                    avaliable[i] += itr.second.allocated[i];
                notDone = true;
            }
        }

        /* Delete the finished processes from the system */
        for(int i = 0; i < deleteIndices.size(); ++i)
            processes_map_tmp.erase(deleteIndices[i]);

    }while(notDone);

    return processes_map_tmp.size() == 0;
}

/* Handle new process command */
void newPrcs(std::unordered_map<int, process>* processes_map, int prcsIndex, std::vector<int>* rscArgs, std::vector<int>* avaliable){

    processes_map->emplace(prcsIndex, process(rscArgs));
    if(safeChecking(processes_map, avaliable)){
        std::cout << "OK" << std::endl;
    }else{
        processes_map->erase(prcsIndex); 
        std::cout << "NOT OK" << std::endl;
    }
}

/* Handle request command */
void request(std::unordered_map<int, process>* processes_map, int prcsIndex, std::vector<int>* rscArgs, std::vector<int>* avaliable){

    /* Should not larger than the avaliable resources */
    if( ! isRscSmallerOrEqual(rscArgs, avaliable)){
        std::cout << "NOT OK" << std::endl;
        return;
    }
    
    /* Should not larger than the MAX resources */
    if( ! isRscSmallerOrEqual(rscArgs, &(processes_map->find(prcsIndex)->second.max))){
        std::cout << "NOT OK" << std::endl;
        return;
    }

    /* Allocate resources to see whether this state is ok ot not */
    for(int i = 0; i < rscArgs->size(); ++i){
        processes_map->find(prcsIndex)->second.allocated[i] += (*rscArgs)[i];
        (*avaliable)[i] -= (*rscArgs)[i];
    }

    /* Not safe, give back the resources */
    if( ! safeChecking(processes_map, avaliable)){
        for(int i = 0; i < rscArgs->size(); ++i){
            processes_map->find(prcsIndex)->second.allocated[i] -= (*rscArgs)[i];
            (*avaliable)[i] += (*rscArgs)[i];
        }
        std::cout << "NOT OK" << std::endl;

    }else{ /* OK */
        std::cout << "OK" << std::endl;
    }
}

/* Handle terminate command */
void terminate(std::unordered_map<int, process>* processes_map, int prcsIndex, std::vector<int>* available){
    std::unordered_map<int, process>::iterator itr = processes_map->find(prcsIndex); 
    if(itr == processes_map->end()){
        std::cout << "Process "<< prcsIndex <<" not found. Exit" << std::endl;
        exit(-1);
    }

    processes_map->erase(itr);
    for(int i = 0; i < itr->second.allocated.size(); ++i)
        (*available)[i] += itr->second.allocated[i];

    std::cout << "OK" << std::endl; // Always glad to recover resources.
}

int main(){

    bool debug = false;

#ifdef BANKER_DEBUG 
    std::streambuf *backup;  
    std::ifstream fin;  
    fin.open("Sample2.in");  /* debug: read from file */   
    std::cin.rdbuf(fin.rdbuf()); 
#endif

    /* Prepare data structures */
    std::unordered_map<int, process> processes_map; // process id : process

    /* Read Inputs */
    int numRscTyp;
    std::cin >> numRscTyp;

    /* The number of resource types */
    std::vector<int> rscTyps; // store the total number of all resources.
    std::vector<int> avaliable; // keep tracking the current available resources.
    
    int tmp;
    /* The maximum quantity of each resource */
    for(int i = 0; i < numRscTyp; ++i){
        std::cin >> tmp;
        rscTyps.push_back(tmp);
    }
    avaliable.assign(rscTyps.begin(), rscTyps.end());
    
    /* Handle commands */
    int prcsIndex;
    char command[10];
    std::vector<int> rscArgs;

    while(std::cin >> prcsIndex >> command){
        rscArgs.clear();
        if(strcmp(command, "terminate") == 0){ /* Terminate process */
            terminate(&processes_map, prcsIndex, &avaliable);

        }else{
            if(strcmp(command, "new") == 0 || strcmp(command, "request") == 0){
                for(int i = 0; i < numRscTyp; ++i){
                    std::cin >> tmp;
                    rscArgs.push_back(tmp);
                }

                if(strcmp(command, "new") == 0){ /* New process */
                    newPrcs(&processes_map, prcsIndex, &rscArgs, &avaliable);

                }else{ /* Process request for resources */
                    request(&processes_map, prcsIndex, &rscArgs, &avaliable);
                }
            }else{ /* For debug */
                debug =! debug;
            }
        }
        if(debug){
            std::cout << "=============="<< prcsIndex <<" "<<command <<"==============" << std::endl;
            debugMap(&processes_map, numRscTyp, &rscTyps, &avaliable);
            std::cout << "=======================================" << std::endl;
        }
    }
    return 0;
}