#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>

#include <opencv2/opencv.hpp>

using namespace std;

class KevinCamera
{
public:
    KevinCamera();
    key_t key;
    int shmid;
    void setShmid(int key);
};

KevinCamera::KevinCamera()
{

}

void KevinCamera::setShmid(int key)
{
    KevinCamera::key = key;
    cout << "key: " << key << "\n";

    KevinCamera::shmid = shmget(KevinCamera::key, 1024, 0666 | IPC_CREAT);
    cout << "shmid: " << shmid << "\n";

}

int main()
{
    KevinCamera camera1;
    KevinCamera camera2;

    camera1.setShmid(0x881);
    camera2.setShmid(0x882);

    while (1)
    {
        // shmat to attach to shared memory
        cv::Point *shm_point1 = (cv::Point *)shmat(camera1.shmid, (void *)0, 0);
        cv::Point *shm_point2 = (cv::Point *)shmat(camera2.shmid, (void *)0, 0);

        cout << "1: ";
        for (int i = 0; i < 10; i++)
        {
            cout << shm_point1[i] << " ";
        }
        cout << "\n2: ";
        for (int i = 0; i < 10; i++)
        {
            cout << shm_point2[i] << " ";
        }
        cout << "\n";

        //detach from shared memory
        shmdt(shm_point1);
        shmdt(shm_point2);
    }

    return 0;
}