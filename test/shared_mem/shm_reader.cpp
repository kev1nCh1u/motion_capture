#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
using namespace std;
  
int main()
{
    // ftok to generate unique key
    // key_t key = ftok("./build/shm_writer",65);
    key_t key = 0x12345;
    cout << "key: " << key << "\n";
  
    // shmget returns an identifier in shmid
    int shmid = shmget(key,1024,0666|IPC_CREAT);
    cout << "shmid: " << shmid << "\n";

    int count = 0;

    while(1)
    {
        // shmat to attach to shared memory
        int *shmVar = (int*) shmat(shmid,(void*)0,0);

        cout << count  << ": ";
        
        for(int i=0; i<10; i++)
        {
            cout << shmVar[i] << " ";
        }
        cout << "\n";

        //detach from shared memory 
        shmdt(shmVar);

        count++;
    }

    // destroy the shared memory
    // shmctl(shmid,IPC_RMID,NULL);
     
    return 0;
}