#ifdef __unix__
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#endif
#include "StreamRetrieve.h"
#include "GenICam/Frame.h"
#include "Media/RecordVideo.h"
#include "Media/ImageConvert.h"

#include <opencv2/opencv.hpp>

extern HANDLE g_hHandle;

StreamRetrieve::StreamRetrieve(IStreamSourcePtr& streamSptr)
	: CThread("streamRetrieve")
	, m_isLoop(false)
	, m_streamSptr(streamSptr)
	, m_bThreadFinished(false)
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
	while (m_bThreadFinished == false)
    {
        CThread::sleep(100);
    }
	m_streamSptr.reset();
	return destroyThread();
}

void StreamRetrieve::threadProc()
{
	int frameCount = 0;
	while (m_isLoop)
	{
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

		// 打印FrameID
		// print frame ID
		printf("get frame %d successfully thread ID :%d\n", ++frameCount, CThread::getCurrentThreadID());
	
		if (g_hHandle)
		{
		    RECORD_SFrameInfo frameInfo;
		    frameInfo.data = (const unsigned char*)frame.getImage();
		    frameInfo.size = frame.getImageSize();
		    frameInfo.paddingX = frame.getImagePadddingX();
		    frameInfo.paddingY = frame.getImagePadddingY();
		    frameInfo.pixelformat = frame.getImagePixelFormat();

		    // 录制一帧图像
		    // record one frame
		    if (RECORD_SUCCESS == inputOneFrame(g_hHandle, &frameInfo))
		    {
		        printf("record frame %d successfully thread ID :%d\n", frameCount, CThread::getCurrentThreadID());
		    }
		}


		/*****************************************************************************************************************
		 *  kevin catch frame
		 * **************************************************************************************************************/
		std::cout << frame.getImagePixelFormat() << "\n";
		/* 转码 */
		uint8_t *pRGBbuffer = NULL;
		int nRgbBufferSize = 0;
		nRgbBufferSize = frame.getImageWidth() * frame.getImageHeight() * 3;
		pRGBbuffer = (uint8_t *)malloc(nRgbBufferSize);
		if (pRGBbuffer == NULL)
		{
			/* 释放内存 */
			printf("RGBbuffer malloc failed.\n");
			continue;
		}

		IMGCNV_SOpenParam openParam;
		openParam.width = frame.getImageWidth();
		openParam.height = frame.getImageHeight();
		openParam.paddingX = frame.getImagePadddingX();
		openParam.paddingY = frame.getImagePadddingY();
		openParam.dataSize = frame.getImageSize();
		openParam.pixelForamt = frame.getImagePixelFormat();

		uint8_t *pSrcbuffer = NULL;
		pSrcbuffer = (uint8_t *)malloc(nRgbBufferSize);

		IMGCNV_EErr status = IMGCNV_ConvertToBGR24(pSrcbuffer, &openParam, pRGBbuffer, &nRgbBufferSize);
		if (IMGCNV_SUCCESS != status)
		{
			/* 释放内存 */
			printf("IMGCNV_Convert failed.\n");
			free(pRGBbuffer);
			return;
		}
		printf(" kevin catch frame finish ...\n");

		cv::imshow("get_frame", image);
		cv::waitKey(1);
		/************************************************************************************************************************/

	}

	m_bThreadFinished = true;
	
}


