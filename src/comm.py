import paho.mqtt.client as mqtt
import re

server_id = 'aws'

class Comm:
    remotes = []
    is_there_server = False
    on_change = lambda: None
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

    # The callback for when the client receives a CONNACK response from the server.
    @staticmethod
    def on_connect(client, userdata, rc):
        print("Start collecting data...")
        client.subscribe("status/server/" + server_id)
        client.subscribe("status/device/+")
        pass

    # The callback for when a PUBLISH message is received from the server.
    @staticmethod
    def on_message(client, userdata, msg):
        print("Topic: "+msg.topic+"\n\tPayload: "+str(msg.payload))
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
            if add_or_remove:
                Comm.remotes.append(device_num)
                print(str(device_num) + ' added!')
            else:
                Comm.remotes.remove(device_num)
                print(str(device_num) + ' Deleted')
            print('Now '+str(Comm.remotes))
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

if __name__ == "__main__":
    comm = Comm(host="ec2-52-23-213-20.compute-1.amazonaws.com", on_change=on_change)

    # Infinite loop
    while True:
        pass




