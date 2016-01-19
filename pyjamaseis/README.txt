PyjAmaseis was written using Python 2.7.8 -  

The current version is v2.0 (2016). v1.0 written by Saketh Vishnubhotla, 2014.

PyjAmaseis should run as a *.py file on Windows, Linux, and Mac operating systems, provided Python 2 and the correct modules
have been installed (many should already be in the python libraries if python is installed). The current version can be downloaded
and run via the python command at the terminal. Note that PyjAmaseis has been written as helicorder software for the TC-1 seismometer,
but could be developed to accommodate different models of amateur seismometers.

The bash shell script module-installer.sh can be run as 'sudo bash module-installer.sh' on linux operating systems to install most of the
required modules.

PyjAmaseis has been inspired by the cross-platform java-based school seismology software jAmaSeis: https://www.iris.edu/hq/Wiki/Introduction

Note: PyjAmaseis will not run unless all the required modules are installed:

matplotlib
numpy
sys
platform
Tkinter
tkMessageBox (should come with tkinter)
time
serial
obspy
datetime
decimal
multiprocessing
pyscreenshot
threading
wx
pygeocoder
os
errno
glob
fileinput
pycurl
base64



There are several modules not named here that need to also be installed, to know what these are first install all
the above modules, then run PyjAmaseis and the required modules will be notified to you via the following error:
“ImportError: No module named …”. Most of these remaining modules can be found here - http://www.lfd.uci.edu/~gohlke/pythonlibs/ and https://wiki.python.org/moin/UsefulModules
