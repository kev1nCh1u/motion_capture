# motion_capture

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
    python3.8 src/gui/qt_gui/src/main.py

    python3.8 src/image_processing/capture/single_capture.py