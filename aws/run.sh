#!/bin/bash

mosquitto -c broker.conf
python mqtt-server.py
