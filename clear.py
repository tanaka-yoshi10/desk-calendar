#!/usr/bin/python3
import sys
import os
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'epd')
if os.path.exists(libdir):
    sys.path.append(libdir)
import epd7in5_V2

epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()
epd.sleep()
print("e-Paper clear & sleep done.")