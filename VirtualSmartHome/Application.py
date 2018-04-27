import paho.mqtt.client as mqtt

sub_temp = "home/temperature"
sub_humi = "home/humidity"
sub_person = "home/person"

isPerson = 0
temperature = 0
humidity = 0

mqttc = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Application Connected.")
    client.subscribe(sub_temp)
    client.subscribe(sub_humi)
    client.subscribe(sub_person)

def on_message(client, userdata, msg) :
    global isPerson
    global temperature
    global humidity

    topic = msg.topic
    if topic == sub_person :
        isPerson = msg.payload.decode('ascii')
        controll_lamp(isPerson)

    else :
        if topic == sub_temp :
            temperature = int(msg.payload.decode('ascii'))
        elif topic == sub_humi :
            humidity = int(msg.payload.decode('ascii'))

        controll_aircon(temperature, humidity)

def controll_lamp(isPerson) :
    if isPerson is 1 :
        mqttc.publish("home/controll/lamp", "ON")
    else :
        mqttc.publish("home/controll/lamp", "OFF")

def controll_aircon(T, RH) :
    # T = 기온, RH = 상대습도
    discomfort_index = (9/5)*T - 0.55*(1-RH)*((9/5)*T-26) + 32
    level = get_level(discomfort_index)
    controll_dict = {"Very High" : "START", "High" : "START", "Low" : "STOP"}

    if isPerson is 0 :
        mqttc.publish("home/controll/aircon", "STOP")

    else :
        mqttc.publish("home/controll/aircon", controll_dict[level])

    print(round(discomfort_index,2), "(" + level + ")", "[temperature :", T, "humidity :", RH)

def get_level(discomfort_index) :
    if discomfort_index >= 80 :
        level = "Very High"
    elif discomfort_index >= 75 :
        level = "High"
    elif discomfort_index >= 68 :
        level = "Normal"
    else :
        level = "Low"
    return level

def start_mqtt(host="localhost", port=1883, abc=60) :
    mqttc.on_connect = on_connect
    mqttc.connect(host, port, abc)
    mqttc.loop_start()

start_mqtt()

