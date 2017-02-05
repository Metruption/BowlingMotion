import paho.mqtt.client as mqtt
import re
import json
import time

server_id = 'aws'

class Comm:
    remotes = []
    is_there_server = False
    on_change = lambda: None
    sensor_data = {}
    def __init__(self, host, on_change, id='game'):
        # members
        Comm.client = mqtt.Client(client_id=id)

        # MQTT connecting
        # This will msg will discard its topic
        Comm.client.will_set(topic="status/server/" + id, payload='', qos=0, retain=True)
        Comm.client.on_connect = Comm.on_connect
        Comm.client.on_message = Comm.on_message

        try:
            Comm.client.connect(host=host, port=1883, keepalive=60)
        except:
            print('Failed to connect to the server')
            exit()
        else:
            print('Connection Success!')
            Comm.client.publish(topic="status/server/" + id, payload="1", retain=True)

        # Start mqtt Comm.client
        Comm.client.loop_start()
        pass

    def get_remotes(self):
        return Comm.remotes

    def get_data_now(self, id):
        obj = Comm.sensor_data[id].copy()
        obj.pop("last_updated")
        return obj

    def get_data_wait(self, id):
        start_time = Comm.sensor_data[id]["last_updated"]
        while start_time == Comm.sensor_data[id]["last_updated"]:
            pass
        return self.get_data_now(id)

    # The callback for when the client receives a CONNACK response from the server.
    @staticmethod
    def on_connect(client, userdata, rc):
        print("Start collecting data...")
        client.subscribe("status/server/" + server_id)
        client.subscribe("status/device/+")
        client.subscribe("device/+")
        pass

    # The callback for when a PUBLISH message is received from the server.
    @staticmethod
    def on_message(client, userdata, msg):
        # print("Topic: "+msg.topic+"\n\tPayload: "+str(msg.payload))
        is_changed = False
        # Update server status
        if ("status/server/" + server_id) == msg.topic:
            if msg.payload.decode() == "1":
                Comm.is_there_server = True
                print("Server connected!")
            else:
                Comm.is_there_server = False
                print("Server disconnected!")
            is_changed = True
        # Add remotes
        if (re.match("status/device/\d*", msg.topic)):
            add_or_remove = False
            if msg.payload.decode() == "1":
                add_or_remove = True
            device_num = int(msg.topic[len("status/device/"):])
            if add_or_remove and (device_num not in Comm.remotes):
                Comm.remotes.append(device_num)
                Comm.sensor_data[device_num] = {"last_updated":time.time()}
                print(str(device_num) + ' added!')
                is_changed = True
            elif add_or_remove and (device_num in Comm.remotes):
                # No change
                pass
            else:
                Comm.remotes.remove(device_num)
                Comm.sensor_data.pop(device_num)
                print(str(device_num) + ' Deleted')
                is_changed = True
            print('Now '+str(Comm.remotes))
        # Update remote sensor data
        if (re.match("device/\d*", msg.topic)):
            device_num = int(msg.topic[len("device/"):])
            data = json.loads(msg.payload)
            # Last updated time
            data["last_updated"] = time.time()
            Comm.sensor_data[device_num] = data
            #print('Data from '+ str(device_num) + ": " + str(data))
            is_changed = True
        # Trigger event
        if is_changed:
            Comm.on_change()
        pass
'''
    # Connect remotes
    def connect_remotes(self, time=30):
        import time
        start_time = int(time.time())
        t = start_time
        print('Searching for remotes...')
        self.client.subscribe("status/device/+")
        while t < (start_time + time):
            pass
        print('Searching complete!')
        self.client.unsubscribe("status/device/+")
        ##
'''

def on_change():
    print("Something changed")
    pass

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    comm = Comm(host="ec2-52-23-213-20.compute-1.amazonaws.com", on_change=on_change)
    # wait for 5 second.
    time.sleep(3)

    # init plot
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_zlim(-15, 15)
    plt.ion()
    line, = ax.plot([0], [0], [0], label='accelometer curve')
    ax.legend()

    # Infinite loop
    while True:
        for dev_id in comm.get_remotes():
            print("wait for " + str(dev_id) + "...")
            data = comm.get_data_wait(dev_id)
            print("Data taken: " + str(data))
            # Plot
            x = data["x"]
            y = data["y"]
            z = data["z"]
            line.set_xdata(x)
            line.set_ydata(y)
            line.set_3d_properties(z)
            fig.canvas.draw()
            plt.show()
