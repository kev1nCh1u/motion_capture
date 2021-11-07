cmake_minimum_required(VERSION 2.8)
project( DisplayImage )

# opencv
# set(OpenCV_DIR /home/kevin/lib/opencv/opencv3/build)
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

# Boost python
find_package(PythonLibs 3.8 REQUIRED)
find_package(Boost COMPONENTS python REQUIRED)
set(CMAKE_SHARED_MODULE_PREFIX "")

# ir_track
add_executable( ir_track src/ir_track.cpp )
target_link_libraries( ir_track ${OpenCV_LIBS})

# boost py ir_track_boostpy
add_library(ir_track_boostpy MODULE src/ir_track_boostpy.cpp)
target_link_libraries(ir_track_boostpy ${OpenCV_LIBS} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
target_include_directories(ir_track_boostpy PRIVATE ${PYTHON_INCLUDE_DIRS})

# test
ADD_LIBRARY(LibsModule 
    src/ir_track.cpp
)
add_executable( test src/test.cpp )
target_link_libraries( test ${OpenCV_LIBS} LibsModule)