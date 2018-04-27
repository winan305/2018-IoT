import paho.mqtt.client as mqtt

mqttc = mqtt.Client()

def on_connect(client, userdata, flags, rc) :
    print("Lamp Controller Connected.")
    client.subscribe("home/controll/lamp")

def on_message(client, userdata, msg) :
    data = msg.payload.decode('ascii')
    controll(data)

def controll(controll_msg) :
    if controll_msg == "ON" :
        print("Light ON")

    elif controll_msg == "OFF" :
        print("Light OFF")

def start_mqtt(host="localhost", port=1883, abc=60) :
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(host, port, abc)
    mqttc.loop_forever()

start_mqtt()
