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


###########
# 分頁視窗 #
###########
# gnome-terminal --tab -t "分頁名稱" -- bash -ic "指令"
gnome-terminal --tab -t "roscore" -- bash -ic "roscore"
sleep 0.2
gnome-terminal --tab -t "camera_0" -- bash -ic "./src/image_processing/dahua_cpp/sample 4H05A85PAK641B0 881"
sleep 0.2
gnome-terminal --tab -t "camera_1" -- bash -ic "./src/image_processing/dahua_cpp/sample 4H05A85PAK7178C 882"
sleep 1
gnome-terminal --tab -t "point2world" -- bash -ic "./src/image_processing/light_track/build/ros2_point2world"
sleep 0.2
