import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, msg) :
    print("Topic :", msg.topic, "\nMessage :", str(msg.payload))
    for i in range(100000) :
        print(i)

def on_connect(client, userdata, flags, rc) :
    client.subscribe("paho/temperature")
    
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("127.0.0.1", 1883, 60)
mqttc.loop_forever()

