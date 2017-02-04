#!/bin/sh

# install dependancy of mosquitto
sudo sh -c "echo 'deb http://us.archive.ubuntu.com/ubuntu vivid main universe' >> /etc/apt/sources.list"
sudo apt-get update
sudo apt-get install libwebsockets3

# install mosquitto
sudo wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
sudo apt-key add mosquitto-repo.gpg.key
cd /etc/apt/sources.list.d/
sudo wget http://repo.mosquitto.org/debian/mosquitto-stretch.list  # In case of you use debian Jessie (ubuntu 14.04 or higher). If you use stretch (or ubuntu 16.04) download mosquitto-stretch instead.
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install python-setuptools python-dev build-essential
sudo apt-get install python-pip
sudo pip install paho-mqtt
