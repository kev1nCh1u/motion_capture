#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
using namespace std;
  
int main()
{
    // ftok to generate unique key
    key_t key = ftok("./build/shm_writer",65);
    cout << key << "\n";
  
    // shmget returns an identifier in shmid
    int shmid = shmget(key,1024,0666|IPC_CREAT);
  
    // shmat to attach to shared memory
    // char *qq = (char*) shmat(shmid,(void*)0,0);
    // cout<<"Write Data : ";
    // std::cin >> qq;
    // printf("Data written in memory: %s\n",qq);

    int *qq = (int*) shmat(shmid,(void*)0,0);
    for(int i=0; i<1024; i++)
    {
        qq[i] = i+1;
    }
      
    //detach from shared memory 
    shmdt(qq);
  
    return 0;
}