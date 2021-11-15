#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
using namespace std;
  
int main()
{
    // ftok to generate unique key
    key_t key = ftok("./build/shm_writer",65);
  
    // shmget returns an identifier in shmid
    int shmid = shmget(key,1024,0666|IPC_CREAT);

    // shmat to attach to shared memory
    // char *qq = (char*) shmat(shmid,(void*)0,0);
    // printf("Data read from memory: %s\n",qq);

    int *qq = (int*) shmat(shmid,(void*)0,0);
    cout << "array size: " << sizeof(qq) << endl;
    for(int i=0; i<1024; i++)
    {
        cout << qq[i] << " ";
    }

    //detach from shared memory 
    shmdt(qq);
    
    // destroy the shared memory
    shmctl(shmid,IPC_RMID,NULL);
     
    return 0;
}