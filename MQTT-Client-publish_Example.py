import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc) :
    client.subscribe("res/a")
    
def on_message(client, userdata, msg) :
    print("Topic :", msg.topic, "\nMessage :", str(msg.payload))
    time.sleep(3)
    
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("192.168.0.22", 1883, 60)
mqttc.loop_start()

while True :
    data1 = "data1"
    data2 = "data2"
    data3 = "data3"
    print(data1, data2, data3)
    mqttc.publish("sensor/temp", data1)
    time.sleep(2)

    