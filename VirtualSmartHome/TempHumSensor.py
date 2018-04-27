import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc) :
    print("Human Sensor Connected.")

def generate_data() :
    pass


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.connect("localhost", 1883, 60)
mqttc.loop_forever()

