#ifdef __unix__
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#endif
#include "StreamRetrieve.h"
#include "GenICam/Frame.h"
#include "Media/ImageConvert.h"

#include <opencv2/opencv.hpp>
#include "ir_track.cpp"
#include <chrono>

#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>

#include <signal.h> // signal functions

using namespace std;

extern IMGCNV_HANDLE g_handle;

int shmid_point;

StreamRetrieve::StreamRetrieve(IStreamSourcePtr& streamSptr)
	: CThread("streamRetrieve")
	, m_isLoop(false)
	, m_streamSptr(streamSptr)
{
	
}

bool StreamRetrieve::start()
{
	m_isLoop = true;
	return createThread();
}

bool StreamRetrieve::stop()
{
	m_isLoop = false;
	m_streamSptr.reset();
	return destroyThread();
}

/****************************************************************
 * exit
 * **************************************************************/
static void my_handler(int sig) // can be called asynchronously
{
    cout << "\n";
    cout << "shmid_point: " << shmid_point << "\n";
    
    // destroy the shared memory
    shmctl(shmid_point,IPC_RMID,NULL);

    cout << "Exit\n";
    exit(0);
}

/****************************************************************
 * print array
 * **************************************************************/
void printArr(int arrSize, float arr[])
{
    for(int i = 0; i < arrSize; i++)
    {
        std::cout << arr[i] << " ";
    }
    std::cout << "\n";
}

/****************************************************************
 * push new value in array, and rmove oldest
 * **************************************************************/
void pushNew(int arrSize, float arr[], float newVal)
{
    for(int i = 0; i < arrSize - 1; i++)
    {
        arr[i] = arr[i+1];
    }
    arr[arrSize - 1] = newVal;
}

/****************************************************************
 * calculate array average
 * **************************************************************/
float avgArrFuc(int arrSize, float arr[])
{
    float sumArr = 0;
    float avgArr = 0;

    for(int i = 0; i < arrSize; i++)
    {
        sumArr += arr[i];
    }
    
    avgArr = sumArr / arrSize;
    return avgArr;
}

/****************************************************************
 * threadProc
 * **************************************************************/
void StreamRetrieve::threadProc()
{
	signal(SIGINT, my_handler); 

	int avgFpsSize = 100;
	float hisFps[avgFpsSize];

	// kevin define
	cv::Mat image;
	image = cv::imread("../../../data/ir/Pic_2021_10_09_104654_1.bmp", 1); // ??????????????????
	unsigned int frameCount = 0;

	// kevin shared memory
	// key_t key = 0x888;
	key_t key = shmid_point_id_input;
	cout << "key: " << key << "\n";
	shmid_point = shmget(key,1024,0666|IPC_CREAT); // shmget returns an identifier in shmid
	cout << "shmid: " << shmid_point << "\n";
	cv::Point *shm_point = (cv::Point*) shmat(shmid_point,(void*)0,0); // shmat to attach to shared memory

	while (m_isLoop)
	{
		// kevin define
		printf("=============================================================\n");
		auto start = std::chrono::high_resolution_clock::now();

		// ???frame??????????????????????????????????????????????????????????????????????????????
		// ????????????????????????????????????:?????????????????????????????????????????????????????????????????????
		// ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
		// This frame object must be a temporary variable, and its lifecycle is related to the drive frame cache.
		// The end of this object's life cycle means that the driver can reclaim this frame cache and use it to store subsequent acquired frames.
		// If it is not released in time, the acquired frame will be the same as the set frame cache, and the frame will not be acquired (because the driver has no available frame cache).	
		CFrame frame;

		// ????????????
	    // Get one frame
		if (!m_streamSptr)
		{
			printf("m_streamPtr is NULL.\n");
			return;
		}
		bool isSuccess = m_streamSptr->getFrame(frame, 300);
		if (!isSuccess)
		{
			printf("getFrame  fail.\n");
			continue;
		}

		// ?????????????????????
		// Judge the validity of frame
		bool isValid = frame.valid();
		if (!isValid)
		{
			printf("frame is invalid!\n");
			continue;
		}

		/******************************************************************
		 *  kevin get frame
		 * ****************************************************************/
#ifdef DEBUG
		frameCount++;
		printf("get frame %d...\n", frameCount);
#endif

		// get source buffer
		unsigned char* pSrcbuffer = NULL;
		pSrcbuffer = (unsigned char*)malloc(frame.getImageSize());
		// pSrcbuffer = (unsigned char*)frame.getImage();
		memmove(pSrcbuffer, frame.getImage(), frame.getImageSize());
		cv::Mat bayerMat(frame.getImageHeight(), frame.getImageWidth(), CV_8UC1, pSrcbuffer);

		// opencv show
		// cv::imshow("bayerMat", bayerMat);
		// cv::waitKey(1);

		/******************************************************************
		 *  kevin track
		 * ****************************************************************/
		// opencv Convert the Bayer data to 8-bit RGB
		cv::Mat rgbMat(frame.getImageHeight(), frame.getImageWidth(), CV_8UC3);
		cv::cvtColor(bayerMat, rgbMat, cv::COLOR_BayerGR2RGB);

		std::vector<cv::Point> points;
		// points = ir_track(image, 1, 0);
		points = ir_track(rgbMat, 1, 0);
		std::cout << "points:" << "\n";

		// pub point
		for(size_t i=0; i<points.size(); i++)
		{
			std::cout << points[i] << "\n";
			shm_point[i] = points[i];
		}

		// cv::imshow("get_frame", image);
		// cv::waitKey(1);

		free(pSrcbuffer);

		/******************************************************************
		 *  kevin endTime
		 * ****************************************************************/
		auto stop = std::chrono::high_resolution_clock::now();
		auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
		float currFps = 1. / duration.count() * 1000000;
		pushNew(avgFpsSize, hisFps, currFps);
		float avgFps = avgArrFuc(avgFpsSize, hisFps);

		// ??????FrameID
		// print frame ID
		// printf("get frame %lld successfully thread ID :%d\n", frame.getBlockId(), CThread::getCurrentThreadID());
		printf("get frame %ld successfully thread ID :%d ,fps:%3.2f, avg_fps:%3.2f \n", frame.getBlockId(), CThread::getCurrentThreadID(), currFps, avgFps);
	}

	// kevin shm
    shmdt(shm_point); // shm detach from shared memory 
    shmctl(shmid_point,IPC_RMID,NULL); // destroy the shared memory

}


