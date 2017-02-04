#!/bin/sh

sudo wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
sudo apt-key add mosquitto-repo.gpg.key
cd /etc/apt/sources.list.d/
sudo wget http://repo.mosquitto.org/debian/mosquitto-jessie.list  # In case of you use debian Jessie (ubuntu 14.04 or higher). If you use stretch (or ubuntu 16.04) download mosquitto-stretch instead.
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install python-setuptools python-dev build-essential
sudo apt-get install python-pip
sudo pip install paho-mqtt
sudo apt-get install python-dev libmysqlclient-dev
sudo apt-get install python-mysql.connector
