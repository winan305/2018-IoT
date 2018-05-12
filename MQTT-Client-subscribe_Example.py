import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, msg) :
    print("Topic :", msg.topic, "\nMessage :", str(msg.payload))
    mqttc.publish("res/a", "OK")
    time.sleep(3)

def on_connect(client, userdata, flags, rc) :
    client.subscribe("req/a")
    client.subscribe("req/b")
    client.subscribe("req/c")
    client.subscribe("sensor/temp")
    
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("192.168.0.22", 1883, 60)
mqttc.loop_forever()

