I1 = imread('/home/kevin/src/motion_capture/data/stereo_calibration/new/1/01.jpg');
I2 = imread('/home/kevin/src/motion_capture/data/stereo_calibration/new/2/01.jpg');

[J1, J2] = rectifyStereoImages(I1, I2, stereoParams);
cat_j = cat(2,J1,J2);
figure; imshow(cat_j);

cat_j_size = size(cat_j);
gap = 27;
for i = gap:gap:cat_j_size(1)
    line([0 cat_j_size(2),], [i i]);
end

[J1, J2] = rectifyStereoImages(I1, I2, stereoParams, 'OutputView','full');
Anaglyph = stereoAnaglyph(J1,J2);
figure; imshow(Anaglyph)

imtool(Anaglyph);