#ifndef _IR_TRACK_
#define _IR_TRACK_

#include <stdio.h>
#include <iostream>
#include <opencv2/opencv.hpp>

/**************************************************************************
 * ir_track
 * ************************************************************************/
std::vector<cv::Point> ir_track(cv::Mat image, bool capFlag=1, bool showFlag=0)
{
#ifdef DEBUG
	std::cout << "ir_track..." << std::endl;
#endif
	if(showFlag)
	{
		cv::imshow("original_frame", image);
		cv::waitKey(0);
	}

	cv::cvtColor(image, image, cv::COLOR_BGR2GRAY);
	if(showFlag)
	{
		cv::imshow("gray_image", image);
		cv::waitKey(0);
	}

	cv::threshold(image,image,80,255,0);
	if(showFlag)
	{
		cv::imshow("threshold", image);
		cv::waitKey(0);
	}

	std::vector<std::vector<cv::Point>> contours;
	cv::findContours(image,contours,cv::RETR_TREE,cv::CHAIN_APPROX_SIMPLE);
	if(showFlag)
	{
		for (size_t i=0; i<contours.size(); ++i)
		std::cout << contours[i] << ' ';
		std::cout << "\n";
	}

	// std::vector<cv::Moments> mu(contours.size());
	cv::Moments m;
	std::vector<cv::Point> points(contours.size());
    for(size_t i = 0; i < contours.size(); i++)
    {
        // mu[i] = moments(contours[i]);
		m = cv::moments(contours[i]);
		if(m.m00 > 0)
		{
			points[i].x = m.m10 / m.m00;
			points[i].y = m.m01 / m.m00;
			if(showFlag)
			{
				std::cout << "center_point: " << points[i].x << " " << points[i].y << "\n";
			}

		}
    }
	return points;
}

/**************************************************************************
 * main
 * ************************************************************************/
// #ifndef _MAIN_
// #define _MAIN_
// int main(int argc, char *argv[])
// {
// 	cv::Mat image;

// 	if (argc != 2)
// 	{
// 		printf("Load defalt image\n");
// 		image = cv::imread("../../../../data/ir/Pic_2021_10_09_104654_1.bmp", 1); // 讀取影像檔案
// 		// image = cv::imread("../../../../data/ir/ir_led_4.bmp", 1); // 讀取影像檔案
// 	}
// 	else
// 	{
// 		printf("Load arg image\n");
// 		image = cv::imread(argv[1], 1);
// 	}

// 	if (!image.data)
// 	{
// 		printf("No image data n");
// 		return -1;
// 	}

// 	// cv::namedWindow("Display Image", cv::WINDOW_AUTOSIZE);
// 	// cv::imshow("Display Image", image);
// 	// cv::waitKey(0);

// 	while(1)
// 	{
// 		std::vector<cv::Point> points;
// 		points = ir_track(image, 1, 0);
// 		for(int i=0; i<points.size(); i++)
// 		{
// 			std::cout << points[i] << "\n";
// 		}
// 	}

// 	return 0;
// }
// #endif

#endif