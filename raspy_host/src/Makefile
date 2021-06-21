prefix := /usr/local

# The recommended compiler flags for the Raspberry Pi
CCFLAGS=-Ofast

# define all programs
PROGRAMS = raspy_host test
SOURCES = ${PROGRAMS:=.cpp}

all: ${PROGRAMS}

${PROGRAMS}: ${SOURCES} raspy_host.h
	g++ ${CCFLAGS} -Wall  -lssd1306 $@.cpp -o $@

clean:
	rm -rf $(PROGRAMS)

install: all
	test -d $(prefix) || mkdir $(prefix)
	test -d $(prefix)/bin || mkdir $(prefix)/bin
	for prog in $(PROGRAMS); do \
	  install -m 0755 $$prog $(prefix)/bin; \
	done

.PHONY: install


