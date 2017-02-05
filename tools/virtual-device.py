#!/bin/python
import paho.mqtt.client as mqtt
import sys
import random
import re

dev_id = str(int(random.random()*10000))
main_server_id = 'aws'
game_server_id = 'game'
is_there_main_server = False
is_there_game_server = False
on_change = lambda: None

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("status/server/+")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global is_there_game_server, is_there_main_server, on_change
    print("Topic: "+msg.topic+"\n\tPayload: "+str(msg.payload))
    is_changed = False
    # Update server status
    if re.match('status/server/.*', msg.topic):
        server_id = msg.topic[len("status/server/"):]
        # Decide existance
        if msg.payload.decode() == "1":
            status_to_change = True
        else:
            status_to_change = False
        # Change server status
        if server_id == main_server_id:
            is_there_main_server = status_to_change
            is_changed = True
        elif server_id == game_server_id:
            is_there_game_server = status_to_change
            is_changed = True
    # Callback
    if is_changed:
        on_change()
    pass

if __name__ == '__main__':
    client = mqtt.Client()
    # This will msg will discard its topic
    client.will_set(topic="status/device/"+dev_id, payload='', qos=0, retain=True)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(host="ec2-52-23-213-20.compute-1.amazonaws.com", port=1883, keepalive=60)
    except:
        print('Failed to connect to the server')
        exit()
    else:
        print('Connection Success!')
        # log in device
        client.publish(topic="status/device/"+dev_id, payload="1", retain=True)

    client.loop_start()

    print('Checking all servers...')
    while not (is_there_main_server and is_there_game_server):
        pass

    print('Connection confirmed!')
    print('Now start publishing sensor value?')
    # Wait
    import time
    while True:
        time.sleep(1000)
    pass
