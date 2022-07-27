# motion_capture

```
 _              _    __     ___     _             
| | _______   _(_)_ _\ \   / (_)___(_) ___  _ __  
| |/ / _ \ \ / / | '_ \ \ / /| / __| |/ _ \| '_ \ 
|   <  __/\ V /| | | | \ V / | \__ \ | (_) | | | |
|_|\_\___| \_/ |_|_| |_|\_/  |_|___/_|\___/|_| |_|
                                            
```

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

## source
    source /home/kevin/src/motion_capture/kevin_setup.bash

## run start
    kevin_start_main.bash

## create markers
    kevin_start_create_markers.bash

## install matlab engine
https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
```
cd "matlabroot\extern\engines\python"
python setup.py install
```

## run dahua
    roscore
    python src/dahua_python/src/ros_cv_getFrame.py

    python src/image_processing/ir_track/src/ros_stero_light_track.py


## dahua track point
    roscore
    kevin_start_capture.bash
    kevin_start_calib.bash

    python src/image_processing/calibration/stereo_depth_Chessboard.py

    kevin_start_stereo_ir_track.bash
    python src/image_processing/ir_track/src/ros_point_record.py

## fpga track point
### calibration quick start
    kevin_start_capture.bash
    kevin_start_calibration.bash
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

### UML
    python3.8 ~/.local/bin/pyreverse -o png src/kevinVision/. -mn -a1