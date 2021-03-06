% matlab_stereo_param
fprintf('\nStart create cv yaml\n')

fileName = "/home/kevin/src/motion_capture/data/parameter/matlab_stereo_param.yaml";
disp(fileName)

matlab2opencv(fileName, stereoParams.CameraParameters1.IntrinsicMatrix, "IntrinsicMatrix1", "w")
matlab2opencv(fileName, stereoParams.CameraParameters1.RadialDistortion, "RadialDistortion1", "a")
matlab2opencv(fileName, stereoParams.CameraParameters1.TangentialDistortion, "TangentialDistortion1", "a")

matlab2opencv(fileName, stereoParams.CameraParameters2.IntrinsicMatrix, "IntrinsicMatrix2", "a")
matlab2opencv(fileName, stereoParams.CameraParameters2.RadialDistortion, "RadialDistortion2", "a")
matlab2opencv(fileName, stereoParams.CameraParameters2.TangentialDistortion, "TangentialDistortion2", "a")

matlab2opencv(fileName, stereoParams.CameraParameters1.ImageSize, "ImageSize", "a")
matlab2opencv(fileName, stereoParams.RotationOfCamera2, "RotationOfCamera2", "a")
matlab2opencv(fileName, stereoParams.TranslationOfCamera2, "TranslationOfCamera2", "a")

matlab2opencv(fileName, stereoParams.CameraParameters1.FocalLength, "FocalLength", "a")

matlab2opencv(fileName, stereoParams.EssentialMatrix, "EssentialMatrix", "a")
matlab2opencv(fileName, stereoParams.FundamentalMatrix, "FundamentalMatrix", "a")

fprintf('Finish...\n')