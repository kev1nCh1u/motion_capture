CROSS_COMPILE = 
CXX = $(CROSS_COMPILE)g++ $(CFLAGS)
CPPFLAGS = -Wall -g
AR=ar

HOST_ARCH=$(shell uname -m | sed -e 's/i.86/i686/' -e 's/^armv.*/arm/')

ifeq ($(HOST_ARCH), x86_64) 
	CPPFLAGS += -m64
	SDK_LIB_SUBDIR=m64x86
else ifeq ($(HOST_ARCH), i686) 
	CPPFLAGS += -m32
	SDK_LIB_SUBDIR=m32x86
else
endif

TARGET = sample

INCLUDES = -I./include/kevin
INCLUDES += -I./include/dahua
LINKLIBS = -L./depends/$(SDK_LIB_SUBDIR) -lMVSDK -lRecordVideo -lavcodec -lavfilter -lavformat -lavutil -lpostproc -lswresample -lswscale -lx264 -lImageConvert -lrt -lpthread
LINKLIBS += -L../../../lib/dahua -lMVSDK -lRecordVideo -lavcodec -lavfilter -lavformat -lavutil -lpostproc -lswresample -lswscale -lx264 -lImageConvert
SOURCES = $(wildcard *.cpp)
OBJECTS = $(patsubst %.cpp, %.o, $(SOURCES))

# opencv
# OPENCV = `pkg-config opencv2 --cflags --libs`
OPENCV = `pkg-config opencv4 --cflags --libs`
LIBS = $(OPENCV)

# flag
# CFLAGS = $(INCS) -dDEBUG
CFLAGS = $(INCS) -dNDEBUG

$(TARGET):$(OBJECTS)
	$(CXX) $(INCLUDES) $(CPPFLAGS) $(OBJECTS) $(LINKLIBS) $(LIBS) $(CFLAGS) -o $(TARGET)
	rm -f $(OBJECTS)
	
.cpp.o:
	$(CXX) $(INCLUDES) -c $(CPPFLAGS) $< -o $@
	
.PHONY: clean
clean:
	rm -f $(OBJECTS) $(TARGET)

	
