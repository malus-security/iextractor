CFLAGS = -Wall
LDLIBS = -lcrypto

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	LDFLAGS = -L/opt/local/lib
	CPPFLAGS = -I/opt/local/include -DMAC_OSX
endif

.PHONY: all clean

all: vfdecrypt

clean:
	-rm -f vfdecrypt
	-rm -f *~
