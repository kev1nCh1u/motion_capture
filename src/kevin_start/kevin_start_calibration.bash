#!/bin/bash
# Program:
#       This program start motion_capture
# History:
# 2022/6/4	kevin	First release

echo -e "\033[32m
##############################
# motion_capture
# by Kevin Chiu 2022
##############################
\033[0m"
ws_path="/home/kevin/src/motion_capture/" # 路徑
# ws_path=$(pwd) # 自動路徑
echo -e "ws_path:" $ws_path "\n" # 列印路徑
cd $ws_path
# source devel/setup.bash


python3.8 src/matlab/start_stero_calib.py

