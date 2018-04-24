import paho.mqtt.client as mqtt
import time
def on_connect(client, userdata, rc) :
    print("Connection returned result : ", connack_string(rc))
    
mqttc = mqtt.Client()
#mqttc.on_connect = on_connect

mqttc.connect("127.0.0.1", 1883, 60)
mqttc.loop_start()

while True :
    data = "team 2"
    print(temperature)
    mqttc.publish("req/game_play", data)
    time.sleep(3)
    