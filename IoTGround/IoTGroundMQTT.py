import paho.mqtt.client as mqtt
import Server

REQ_MESSAGE = ["+/REQ_GAME_START, +/REQ_SHOW_RANKING, +/REQ_SHOW_USERINFO"]
RES_MESSAGE = ["+/RES_GAME_START, +/RES_SHOW_RANKING, +/RES_SHOW_USEINFO, +/RES_SHOW_GAME_RESULT"]

server = Server.Server()

def initMQTT(host="127.0.0.1", port=1883, keepalive=60, bind_addr=""):
    mqtt_client = mqtt.Client()
    # callback functions setting
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect
    #mqttc.on_publish = on_publish
    #mqttc.on_subscribe = on_subscribe
        
    mqtt_client.connect(host, port, keepalive,bind_addr)
    mqtt_client.loop_forever()
    
def on_message(client, userdata, msg) :
    topic = msg.topic
    data = msg.payload.decode('ascii').split()
    process(topic, data)

def on_connect(client, userdata, flags, rc) :
    print("MQTT Client : on_connect")
    for req in REQ_MESSAGE :
        client.subscribe(req)

def process(req, data):
    global server
    request = req.split("/")
    print(request)
    if req == REQ_MESSAGE[0] :
        server.start_game(data)
        
    elif req == REQ_MESSAGE[1] :
        user_info = server.send_user_info(data)
    
    elif req == REQ_MESSAGE[2] :
        ranking = server.send_ranking(data)
        

initMQTT()