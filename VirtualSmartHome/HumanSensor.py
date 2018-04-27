import paho.mqtt.client as mqtt
from random import *
import threading

PUBLISHING_TIME = 2
mqttc = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Human Sensor Connected.")
    publishing(generate_data())

def generate_data():
    isPerson = randrange(2)
    return isPerson

def publishing(data):
    publish_timer = threading.Timer(PUBLISHING_TIME, publishing, args=[generate_data()])
    mqttc.publish("home/person", data)
    print("사람 감지됨" if data is 1 else "사람 감지 안됨")
    publish_timer.start()

def start_mqtt(host="localhost", port=1883, abc=60) :

    mqttc.on_connect = on_connect
    mqttc.connect(host, port, abc)
    mqttc.loop_forever()

start_mqtt()

