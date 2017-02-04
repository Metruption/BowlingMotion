#!/bin/python
import paho.mqtt.client as mqtt
import sys

server_id = 'inspector-0'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    if '--admin' in sys.argv:
        client.subscribe("$SYS/#")
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Topic: "+msg.topic+"\n\tPayload: "+str(msg.payload))

if __name__ == '__main__':
    for idx, arg in enumerate(sys.argv):
        if arg == '--id':
            server_id = 'inspector-' + sys.argv[idx+1]
    client = mqtt.Client(client_id="server_"+server_id)
    client.will_set(topic="status/server/"+server_id, payload="0", qos=0, retain=False)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(host="ec2-52-23-213-20.compute-1.amazonaws.com", port=1883, keepalive=60)
    except:
        print('Failed to connect to the server')
        exit()
    else:
        print('Connection Success!')
        client.publish(topic="status/server/"+server_id, payload="1", retain=True)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    print('Waiting for any messages...')
    client.loop_forever()
    pass
