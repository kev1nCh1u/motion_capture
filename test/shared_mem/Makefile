# opencv
# OPENCV = `pkg-config opencv2 --cflags --libs`
OPENCV = `pkg-config opencv4 --cflags --libs`
LIBS = $(OPENCV)


main:
	g++ shm_writer.cpp -o build/shm_writer
	g++ shm_reader.cpp  -o build/shm_reader
	g++ shm_getPoint.cpp $(LIBS) -o build/shm_getPoint

	