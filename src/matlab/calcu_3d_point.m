point1 = stereoParams.CameraParameters1.ReprojectedPoints(4,:,27);
point2 = stereoParams.CameraParameters2.ReprojectedPoints(4,:,27);

x1 = [stereoParams.CameraParameters1.ReprojectedPoints(4,:,27) 1]';
x2 = [stereoParams.CameraParameters2.ReprojectedPoints(4,:,27) 1]';

tx1 = [379.6703,154.38605];
tx2 = [124.930595,153.90338];

dx = 379.76 - 124.93
dy = 154.39 - 153.90

k1 = [stereoParams.CameraParameters1.IntrinsicMatrix' [0;0;0]];
k1_ = [stereoParams.CameraParameters1.IntrinsicMatrix'];
k = [1,0,0,0;0,1,0,0;0,0,1,0];
k_ = [1,0,0;0,1,0;0,0,1];

f = stereoParams.FundamentalMatrix';
r = stereoParams.RotationOfCamera2';
t = stereoParams.TranslationOfCamera2';

p = k * [[r t];0,0,0,1];

t1 = [320.3  130.2 1442.7 1]';
t1_ = [320.3  130.2 1442.7]';

x1' * f * x2

p * t1
k1_ * r * t1_;

k1_ * [tx1,1]' 

% worldPoints = triangulate(point1,point2,stereoParams)
% worldPoints = triangulate(tx1,tx2,stereoParams)