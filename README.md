# motion_capture

```
 _  __          _        ____ _     _       
| |/ /_____   _(_)_ __  / ___| |__ (_)_   _ 
| ' // _ \ \ / / | '_ \| |   | '_ \| | | | |
| . \  __/\ V /| | | | | |___| | | | | |_| |
|_|\_\___| \_/ |_|_| |_|\____|_| |_|_|\__,_|
                                            
```

## source
    source /home/kevin/src/motion_capture/kevin_setup.bash

## camera
```
          marker
            /\
           /  \
          /    \
         /      \
        /        \
       /          \
    camera_1    camera_2
```
threshold: 100

## led 
V: 3V


## install matlab engine
https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
```
cd "matlabroot\extern\engines\python"
python setup.py install
```

## run start
    source setup.zsh
    kevin_start.zsh

## run code
    roscore
    python src/dahua_python/src/ros_cv_getFrame.py

    python src/image_processing/ir_track/src/ros_stero_light_track.py


## dahua track point
    roscore
    kevin_start_capture.zsh
    kevin_start_calib.zsh

    python src/image_processing/calibration/stereo_depth_Chessboard.py

    kevin_start_stereo_ir_track.zsh
    python src/image_processing/ir_track/src/ros_point_record.py

## fpga track point
### calibration
    python3.8 src/image_processing/capture/double_capture.py
    python3.8 src/matlab/start_stero_calib.py
### verification
    python3.8 src/image_processing/calibration/stereo_board_depth_triangulation.py -id 14

    python3.8 src/image_processing/calibration/get_data.py
    python3.8 src/image_processing/calibration/point_plot_3d.py

### GUI
    python3.8 src/gui/qt_gui/main.py

### test
    python3.8 src/image_processing/capture/single_capture.py