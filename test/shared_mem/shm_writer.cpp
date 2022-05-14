#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
#include <signal.h> // signal functions

using namespace std;

int shmid;

static void my_handler(int sig) // can be called asynchronously
{
    cout << "\n";
    cout << "shmid: " << shmid << "\n";
    
    // destroy the shared memory
    shmctl(shmid,IPC_RMID,NULL);

    cout << "Exit\n";
    exit(0);
}

int main()
{
    signal(SIGINT, my_handler); 

    // ftok to generate unique key
    // key_t key = ftok("./build/shm_writer",65);
    key_t key = 0x12345;
    cout << "key: " << key << "\n";
    
    // shmget returns an identifier in shmid
    shmid = shmget(key,1024,0666|IPC_CREAT);
    cout << "shmid: " << shmid << "\n";

    // shmat to attach to shared memory
    int *shmVar = (int*) shmat(shmid,(void*)0,0);

    int count = 0;

    while(1)
    {
        shmVar[0] = count;
        for(int i=1; i<10; i++)
        {
            shmVar[i] = i;
        }

        for(int i=0; i<10; i++)
        {
            cout << shmVar[i] << " ";
        }
        cout << "\n";
            
        count++;
    }

    //detach from shared memory 
    shmdt(shmVar);
  
    return 0;
}