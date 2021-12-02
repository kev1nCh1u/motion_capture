cmake_minimum_required(VERSION 2.8)
project( DisplayImage )

# opencv
# set(OpenCV_DIR /home/kevin/lib/opencv/opencv3/build)
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

# ir_track
add_executable( ir_track src/ir_track.cpp )
target_link_libraries( ir_track ${OpenCV_LIBS})

# ros2_point2world
add_executable( ros2_point2world src/ros2_point2world.cpp )
target_link_libraries( ros2_point2world ${OpenCV_LIBS})