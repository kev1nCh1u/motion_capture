#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>

#include <opencv2/opencv.hpp>

using namespace std;
  
int main()
{
    // ftok to generate unique key
    // key_t key = ftok("./build/shm_writer",65);
    key_t key = 0x888;
  
    // shmget returns an identifier in shmid
    int shmid = shmget(key,1024,0666|IPC_CREAT);

    // shmat to attach to shared memory
    cv::Point *shm_point = (cv::Point*) shmat(shmid,(void*)0,0);
    cout << "array size: " << sizeof(shm_point) << endl;
    for(int i=0; i<10; i++)
    {
        cout << shm_point[i] << " ";
    }

    //detach from shared memory 
    shmdt(shm_point);
    
    // destroy the shared memory
    shmctl(shmid,IPC_RMID,NULL);
     
    return 0;
}