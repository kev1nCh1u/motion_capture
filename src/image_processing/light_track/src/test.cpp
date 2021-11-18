

#include <stdio.h>
#include <iostream>
#include <opencv2/opencv.hpp>
#include "ir_track.cpp"

/**************************************************************************
 * main
 * ************************************************************************/
#ifndef _MAIN_
#define _MAIN_
int main(int argc, char *argv[])
{
	cv::Mat image;

	if (argc != 2)
	{
		printf("Load defalt image\n");
		image = cv::imread("../../../../img/ir/Pic_2021_10_09_104654_1.bmp", 1); // 讀取影像檔案
		// image = cv::imread("../../../../img/ir/ir_led_4.bmp", 1); // 讀取影像檔案
	}
	else
	{
		printf("Load arg image\n");
		image = cv::imread(argv[1], 1);
	}

	if (!image.data)
	{
		printf("No image data n");
		return -1;
	}

	// cv::namedWindow("Display Image", cv::WINDOW_AUTOSIZE);
	// cv::imshow("Display Image", image);
	// cv::waitKey(0);

	while(1)
	{
		std::vector<cv::Point> points;
		points = ir_track(image, 1, 0);
		for(int i=0; i<points.size(); i++)
		{
			std::cout << points[i] << "\n";
		}
	}

	return 0;
}
#endif