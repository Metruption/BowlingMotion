#!/bin/sh

# Download
wget https://az764295.vo.msecnd.net/stable/27240e71ef390bf2d66307e677c2a333cebf75af/code_1.9.0-1486023356_amd64.deb
# For .deb
sudo dpkg -i code_1.9.0-1486023356_amd64.deb
# install dependencies
sudo apt-get install -f
sudo apt-get install libgtk2.0-0 libgconf-2-4 libxss1 libasound2
