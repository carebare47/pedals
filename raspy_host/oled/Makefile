# Where you want it installed when you do 'make install'
PREFIX=/usr/local

# Library parameters
# where to put the lib
LIBDIR=$(PREFIX)/lib
# lib name 
LIB=libssd1306
# shared library name
LIBNAME=$(LIB).so.1.0

# The recommended compiler flags for the Raspberry Pi
CCFLAGS=-Ofast

# make all
# reinstall the library after each recompilation
all: libssd1306 install

# Make the library
libssd1306: OLED_SSD1306.o OLED_GFX.o bcm2835.o 
	g++ -shared -Wl,-soname,$@.so.1 ${CCFLAGS}  -o ${LIBNAME} $^

# Library parts (use -fno-rtti flag to avoid link problem)
OLED_SSD1306.o: OLED_SSD1306.cpp
	g++ -Wall -fPIC -fno-rtti ${CCFLAGS} -c $^

OLED_GFX.o: OLED_GFX.cpp
	g++ -Wall -fPIC -fno-rtti ${CCFLAGS} -c $^

bcm2835.o: bcm2835.c
	gcc -Wall -fPIC ${CCFLAGS} -c $^

# Install the library to LIBPATH
install: 
	@echo "[Install Library]"
	@if ( test ! -d $(PREFIX)/lib ) ; then mkdir -p $(PREFIX)/lib ; fi
	@install -m 0755 ${LIBNAME} ${LIBDIR}
	@ln -sf ${LIBDIR}/${LIBNAME} ${LIBDIR}/${LIB}.so.1
	@ln -sf ${LIBDIR}/${LIBNAME} ${LIBDIR}/${LIB}.so
	@ldconfig
	@rm -rf ${LIB}.*

	@echo "[Install Headers]"
	@if ( test ! -d $(PREFIX)/include ) ; then mkdir -p $(PREFIX)/include ; fi
	@cp -f  OLED_*.h $(PREFIX)/include
	@cp -f  OLEDType_*.h $(PREFIX)/include
	@cp -f  bcm2835.h $(PREFIX)/include
	
	
# Uninstall the library 
uninstall: 
	@echo "[Uninstall Library]"
	@rm -f ${LIBDIR}/${LIB}.*

	@echo "[Uninstall Headers]"
	@rm -rf  $(PREFIX)/include/OLED_SSD1306*
	@rm -rf  $(PREFIX)/include/OLEDType_SSD1306*
	@rm -rf  $(PREFIX)/include/bcm2835.h
	
# clear build files
clean:
	rm -rf *.o ${LIB}.* ${LIBDIR}/${LIB}.*


