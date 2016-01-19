#!/bin/bash

CODENAME=$(lsb_release -cs)

WX_STRING="## wxWidgets/wxPython repository at apt.wxwidgets.org\ndeb http://apt.wxwidgets.org/ $CODENAME-wx main\ndeb-src http://apt.wxwidgets.org/ $CODENAME-wx main"

sed -i.bak '$ a '"$WX_STRING"'' /etc/apt/sources.list

apt-get update
apt-get -y install python-pip
apt-get -y  install python-setuptools
apt-get -y install python-serial
apt-get -y  install python-easygui
apt-get -y  install python-tk
apt-get -y install python-imaging
apt-get -y install python-numpy
apt-get -y install python-matplotlib
apt-get -y install python-scipy
apt-get -y install python-lxml
apt-get -y install python-sqlalchemy
apt-get -y install libcurl3
apt-get -y install libcurl4-gnutls-dev
apt-get -y install curl

curl http://apt.wxwidgets.org/key.asc | sudo apt-key add -

apt-get -y  install python-wxgtk2.8 python-wxtools wx2.8-i18n

pip install future
pip install obspy
pip install pygeocoder
pip install pyscreenshot

apt-get -y install python-dev
pip install pycurl