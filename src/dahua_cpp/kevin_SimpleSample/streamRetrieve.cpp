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

extern IMGCNV_HANDLE g_handle;

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
	int avgFpsSize = 100;
	float hisFps[avgFpsSize];

	// kevin define
	cv::Mat image;
	image = cv::imread("../../../img/ir/Pic_2021_10_09_104654_1.bmp", 1); // 讀取影像檔案
	unsigned int frameCount = 0;


	while (m_isLoop)
	{
		// kevin define
		printf("=============================================================\n");
		auto start = std::chrono::high_resolution_clock::now();

		// 此frame对象必须为临时变量，对象的生命周期与驱动帧缓存相关。
		// 此对象生命周期结束意味着:驱动可以回收此帧缓存并用于存放后续获取到的帧。
		// 如没有及时释放，获取到的帧与设置的帧缓存相同时，将无法获取到帧（因为驱动已没有可用的帧缓存）。
		// This frame object must be a temporary variable, and its lifecycle is related to the drive frame cache.
		// The end of this object's life cycle means that the driver can reclaim this frame cache and use it to store subsequent acquired frames.
		// If it is not released in time, the acquired frame will be the same as the set frame cache, and the frame will not be acquired (because the driver has no available frame cache).	
		CFrame frame;

		// 获取一帧
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

		// 判断帧的有效性
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
		for(size_t i=0; i<points.size(); i++)
		{
			std::cout << points[i] << "\n";
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

		// 打印FrameID
		// print frame ID
		// printf("get frame %lld successfully thread ID :%d\n", frame.getBlockId(), CThread::getCurrentThreadID());
		printf("get frame %ld successfully thread ID :%d ,fps:%3.2f, avg_fps:%3.2f \n", frame.getBlockId(), CThread::getCurrentThreadID(), currFps, avgFps);
	}

}


