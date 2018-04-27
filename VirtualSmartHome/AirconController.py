import paho.mqtt.client as mqtt

mqttc = mqtt.Client()

def on_connect(client, userdata, flags, rc) :
    print("Aricon Controller Connected.")
    client.subscribe("home/controll/aircon")

def on_message(client, userdata, msg) :
    data = msg.payload.decode('ascii')
    controll(data)

def controll(controll_msg) :
    if controll_msg == "START" :
        print("Start air conditioning")

    elif controll_msg == "STOP" :
        print("Stop air conditioning")

def start_mqtt(host="localhost", port=1883, abc=60) :
    mqttc.on_connect = on_connect
    mqttc.connect(host, port, abc)
    mqttc.loop_start()

start_mqtt()
