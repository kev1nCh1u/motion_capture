#!/bin/zsh
# Program:
#       This program start motion_capture
# History:
# 2021/10/23	kevin	First release

echo -e "\033[32m
##############################
# ros motion_capture   #
# by Kevin Chiu 2021         #
##############################
\033[0m"
ws_path="/home/kevin/src/motion_capture/" # 路徑
# ws_path=$(pwd) # 自動路徑
echo -e "ws_path:" $ws_path "\n" # 列印路徑
cd $ws_path
# source devel/setup.bash

python3 src/image_processing/matlab_calib/start_stero_calib.py
python3 src/image_processing/calibration/stereo_rectify_matlab.py
