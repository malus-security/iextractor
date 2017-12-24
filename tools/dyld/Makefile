CXXFLAGS = -Wall
CXX = clang++

.PHONY: all clean

all: dsc_extractor

dsc_extractor: dsc_extractor.o dsc_iterator.o
	$(CXX) -o $@ $^

clean:
	-rm -f dsc_extractor dsc_extractor.o dsc_iterator.o
	-rm -f *~
