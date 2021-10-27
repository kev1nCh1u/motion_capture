
###########################################################
# cd /usr/local/MATLAB/R2021a/extern/engines/python
# sudo python setup.py install
###########################################################

import os
import time

print('\nCurrent Directory:', os.path.abspath(os.getcwd()))
print('file Directory:', os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print('Change Current Directory To:', os.path.abspath(os.getcwd()))

import matlab.engine
print('\nStart matlab.engine.......')
eng = matlab.engine.start_matlab()
print('\nRun stereo_calib.......')
eng.stereo_calib(nargout=0) # stereo_calib.m
time.sleep(5)
print('\nRun matlabStereo2cvYaml.......')
eng.matlabStereo2cvYaml(nargout=0) # matlabStereo2cvYaml.m
eng.quit()