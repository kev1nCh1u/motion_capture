% Auto-generated by stereoCalibrator app on 26-Oct-2021
%-------------------------------------------------------


% Define images to process
imageFileNames1 = {'/home/kevin/src/motion_capture/data/stereo_calibration/new/1/01.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/02.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/03.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/04.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/05.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/06.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/07.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/08.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/09.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/10.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/11.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/12.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/13.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/14.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/15.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/16.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/17.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/18.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/19.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/20.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/1/21.jpg',...
    };
imageFileNames2 = {'/home/kevin/src/motion_capture/data/stereo_calibration/new/2/01.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/02.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/03.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/04.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/05.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/06.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/07.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/08.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/09.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/10.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/11.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/12.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/13.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/14.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/15.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/16.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/17.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/18.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/19.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/20.jpg',...
    '/home/kevin/src/motion_capture/data/stereo_calibration/new/2/21.jpg',...
    };

% Detect checkerboards in images
[imagePoints, boardSize, imagesUsed] = detectCheckerboardPoints(imageFileNames1, imageFileNames2);

% Generate world coordinates of the checkerboard keypoints
squareSize = 24;  % in units of 'millimeters 10 15 24 40 200'
worldPoints = generateCheckerboardPoints(boardSize, squareSize);

% Read one of the images from the first stereo pair
I1 = imread(imageFileNames1{1});
[mrows, ncols, ~] = size(I1);

% Calibrate the camera
[stereoParams, pairsUsed, estimationErrors] = estimateCameraParameters(imagePoints, worldPoints, ...
    'EstimateSkew', false, 'EstimateTangentialDistortion', false, ...
    'NumRadialDistortionCoefficients', 2, 'WorldUnits', 'millimeters', ...
    'InitialIntrinsicMatrix', [], 'InitialRadialDistortion', [], ...
    'ImageSize', [mrows, ncols]);

% View reprojection errors
h1=figure; showReprojectionErrors(stereoParams);

% Visualize pattern locations
h2=figure; showExtrinsics(stereoParams, 'CameraCentric');

% Display parameter estimation errors
displayErrors(estimationErrors, stereoParams);

% You can use the calibration data to rectify stereo images.
I2 = imread(imageFileNames2{1});
[J1, J2] = rectifyStereoImages(I1, I2, stereoParams);

% See additional examples of how to use the calibration data.  At the prompt type:
% showdemo('StereoCalibrationAndSceneReconstructionExample')
% showdemo('DepthEstimationFromStereoVideoExample')
