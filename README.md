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
    python /home/kevin/src/motion_capture/src/dahua_python/src/ros_cv_getFrame.py

    python /home/kevin/src/motion_capture/src/image_processing/ir_track/src/ros_stero_light_track.py


## dahua track point
    roscore
    kevin_start_capture.zsh
    kevin_start_calib.zsh

    python /home/kevin/src/motion_capture/src/image_processing/calibration/stereo_depth_Chessboard.py

    kevin_start_stereo_ir_track.zsh
    python /home/kevin/src/motion_capture/src/image_processing/ir_track/src/ros_point_record.py

## fpga track point
    python3.8 /home/kevin/src/motion_capture/src/image_processing/capture/multi_capture.py
    python3.8 /home/kevin/src/motion_capture/src/matlab/start_stero_calib.py
    
    python3.8 /home/kevin/src/motion_capture/src/image_processing/calibration/stereo_board_depth_triangulation.py

    python3.8 /home/kevin/src/motion_capture/src/image_processing/calibration/get_data.py
    python3.8 /home/kevin/src/motion_capture/src/image_processing/calibration/point_plot_3d.py