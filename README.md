# motion_capture

## run start
    source setup.zsh
    kevin_start.zsh

## run code
    python /home/kevin/src/motion_capture/src/dahua_python/src/ros_cv_getFrame.py

    python /home/kevin/src/motion_capture/src/image_processing/ir_track/src/stero_ir_track.py


## mission 1
    kevin_start_capture.zsh
    kevin_start_calib.zsh

    python /home/kevin/src/motion_capture/src/image_processing/calibration/stereo_depth_Chessboard.py

    kevin_start_stereo_ir_track.zsh
    python /home/kevin/src/motion_capture/src/image_processing/ir_track/src/point_record.py