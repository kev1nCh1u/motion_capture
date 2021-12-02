#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>

#include <opencv2/opencv.hpp>

using namespace std;

/******************************************************************************************************************
 * KevinCamera
 * ****************************************************************************************************************/
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

/******************************************************************************************************************
 * point2world
 * ****************************************************************************************************************/
class Point2world
{
public:
    Point2world();
    cv::Point3f calcu(cv::Point *left_point, cv::Point *right_point, float baseline, float focal);
    cv::Mat TranslationOfCamera2, FocalLength;
    cv::Mat stereoMapL_x, stereoMapL_y, stereoMapR_x, stereoMapR_y;
};

Point2world::Point2world()
{
    // define
    std::string filename_matlab = "/home/kevin/src/motion_capture/param/matlab_stereo_param.yaml";
    std::string filename_stereoMap = "/home/kevin/src/motion_capture/param/stereoMap.xml";

    // open file
    cout << "Start load param...\n";
    cv::FileStorage matlab_stereo_param(filename_matlab, cv::FileStorage::READ);
    cv::FileStorage stereoMap(filename_stereoMap, cv::FileStorage::READ);

    // open check
    if (!matlab_stereo_param.isOpened())
    {
        cout << "failed to open file " << filename_matlab << endl;
        exit(0);
    }
    if (!stereoMap.isOpened())
    {
        cout << "failed to open file " << filename_stereoMap << endl;
        exit(0);
    }

    // read Mat
    matlab_stereo_param["TranslationOfCamera2"] >> Point2world::TranslationOfCamera2;
    matlab_stereo_param["FocalLength"] >> Point2world::FocalLength;
    stereoMap["stereoMapL_x"] >> Point2world::stereoMapL_x;
    stereoMap["stereoMapL_y"] >> Point2world::stereoMapL_y;
    stereoMap["stereoMapR_x"] >> Point2world::stereoMapR_x;
    stereoMap["stereoMapR_y"] >> Point2world::stereoMapR_y;

    // print
    cout << "Load param finish!\n";
    cout << "Point2world::TranslationOfCamera2: " << Point2world::TranslationOfCamera2.at<float>(0,0);
    exit(0);
    
}

cv::Point3f Point2world::calcu(cv::Point *left_point, cv::Point *right_point, float baseline, float focal)
{
    cout << "Start point2world...\n";

    // point
    cout << "left_point[0]" << left_point[0] << "\n";
    cout << "right_point[0]" << right_point[0] << "\n";

    // displacement between left and right frames [pixels]
    int disparity = abs(left_point[0].x - right_point[0].x);
    float zDepth = (baseline * focal) / disparity; // z depth in [mm]

    cv::Point3f world_points;
    world_points.x = (left_point[0].x * zDepth) / focal;
    world_points.y = (left_point[0].y * zDepth) / focal;
    world_points.z = zDepth;
    return world_points;
}

/******************************************************************************************************************
 * main
 * ****************************************************************************************************************/
int main()
{
    Point2world camera_1_2;
    return 0;

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