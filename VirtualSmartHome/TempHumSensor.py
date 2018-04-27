import paho.mqtt.client as mqtt
from random import *
import threading

PUBLISHING_TIME = 2
mqttc = mqtt.Client()

def on_connect(client, userdata, flags, rc) :
    print("Temperature/Humidity Sensor Connected.")
    publishing(generate_data())

def generate_data() :
    temp = randrange(15, 36)
    humi = randrange(30, 96)/100
    return temp, humi

def publishing(data) :
    publish_timer = threading.Timer(PUBLISHING_TIME, publishing, args=[generate_data()])
    temp, humi = data
    mqttc.publish("home/temperature", temp)
    mqttc.publish("home/humidity", humi)
    print("온도 :", temp, ", 습도 :", humi, "%")
    publish_timer.start()

def start_mqtt(host="localhost", port=1883, abc=60) :
    mqttc.on_connect = on_connect
    mqttc.connect(host, port, abc)
    mqttc.loop_forever()

start_mqtt()
