#!/bin/bash

"""
Script permettant l'installation de gstreamer et de ses plugins necessaires pour notre projet
"""

#definition de la version a installer
BRANCH="1.10"

#mise a jour des repos
sudo apt-get update && sudo apt-get upgrade -y --force-yes

#installations des librairies et logiciels necessaires
sudo apt-get install -y --force-yes pkg-config bison flex git gtk-doc-tools libxv-dev libv4l-dev libx264-dev 

#creation ou utilisation du dossier src_projet puis du sous-dossier gstreamer
cd $HOME
[ ! -d src_projet ] && mkdir src_projet
cd src
[ ! -d gstreamer ] && mkdir gstreamer
cd gstreamer

#recuperation des sources
[ ! -d gstreamer ] && git clone https://github.com/GStreamer/gstreamer.git
[ ! -d gst-plugins-base ] && git clone https://github.com/GStreamer/gst-plugins-base.git
[ ! -d gst-plugins-good ] && git clone https://github.com/GStreamer/gst-plugins-good.git
[ ! -d gst-plugins-ugly ] && git clone https://github.com/GStreamer/gst-plugins-ugly.git
[ ! -d gst-omx ] && git clone https://github.com/GStreamer/gst-omx.git
[ ! -d gst-rtsp-server ] && git clone https://github.com/GStreamer/gst-rtsp-server.git

#compilation des differents plugins
cd gstreamer
git checkout -t origin/$BRANCH || true
./autogen.sh --disable-gtk-doc
make
sudo make install
cd ..

cd gst-plugins-base
git checkout -t origin/$BRANCH || true
./autogen.sh --disable-gtk-doc
make
sudo make install
cd ..

cd gst-plugins-good
git checkout -t origin/$BRANCH || true
./autogen.sh --disable-gtk-doc
make
sudo make install
cd ..

cd gst-plugins-ugly
git checkout -t origin/$BRANCH || true
./autogen.sh --disable-gtk-doc
make
sudo make install
cd ..

cd gst-omx
git checkout -t origin/$BRANCH || true
./autogen.sh --disable-gtk-doc --with-omx-target=rpi --with-omx-header-path=/opt/vc/include/IL
make
sudo make install
cd ..


cd gst-rtsp-server
git checkout -t origin/$BRANCH || true
./autogen.sh --disable-gtk-doc
make
sudo make install
cd ..

fi