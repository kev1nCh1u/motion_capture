
pathVar=$(pwd)
echo "\nNow path:"
echo $pathVar

startPath="${pathVar}/src/kevin_start/src"
echo "\nStart path:"
echo $startPath

PATH=$PATH:$startPath
echo "\nNew system path:"
echo $PATH