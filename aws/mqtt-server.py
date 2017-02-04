#!/bin/python
import paho.mqtt.client as mqtt

server_id = 'aws'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("status/server")
    client.subscribe("status/device")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # This will discard retained message
    client.publish(topic=msg.topic, payload="", retain=True)

if __name__ == '__main__':
    client = mqtt.Client(client_id="server_"+server_id)
    client.will_set(topic="status/server/"+server_id, payload="0", qos=0, retain=True)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(host="127.0.0.1", port=1883, keepalive=60)
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