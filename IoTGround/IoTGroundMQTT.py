import paho.mqtt.client as mqtt
import socket
import time
import threading
import DBManager
from Game import Game

REQ_MESSAGE = ["+/REQ_GAME_START", "+/REQ_SHOW_RANKING", "+/REQ_SHOW_USERINFO", "+/REQ_TEAM_INVITE", "+/INVITE_OK", "+/RESULT_OK"]
RES_MESSAGE = ["/RES_GAME_START", "/RES_SHOW_GAME_RESULT", "/RES_SHOW_RANKING", "/RES_SHOW_USEINFO", "/RES_TEAM_INVITE"]

STATE_FREE = 0
STATE_BUSY = 1
is_invite_ok = False
is_result_ok = []
server_state = STATE_FREE

mqtt_client = mqtt.Client()
dbmanager = DBManager.DBManager()

'''dbmanager.insert_game_result(["01082222910", "20180531", 0.78, 3.51, 2.78, 1.77], DBManager.GAME_MODE_SOLO)
dbmanager.insert_game_result(["01082222910", "20180531", 0.88, 3.31, 2.11, 1.54], DBManager.GAME_MODE_SOLO)
dbmanager.insert_game_result(["01082222910", "20180531", 0.91, 2.51, 1.38, 1.21], DBManager.GAME_MODE_SOLO)
dbmanager.insert_game_result(["01012345678", "20180531", 0.56, 3.51, 2.63, 2.01], DBManager.GAME_MODE_SOLO)
dbmanager.insert_game_result(["01012345678", "20180531", 0.74, 3.11, 2.13, 1.97], DBManager.GAME_MODE_SOLO)
dbmanager.insert_game_result(["01012345678", "20180531", 0.77, 1.78, 1.08, 0.98], DBManager.GAME_MODE_SOLO)
dbmanager.insert_game_result(["01011112222", "20180531", 0.31, 4.15, 3.95, 2.36], DBManager.GAME_MODE_SOLO)
dbmanager.insert_game_result(["01011112222", "20180531", 0.66, 3.31, 2.97, 2.11], DBManager.GAME_MODE_SOLO)
dbmanager.insert_game_result(["01011112222", "20180531", 0.97, 2.11, 1.87, 1.54], DBManager.GAME_MODE_SOLO)'''


'''dbmanager.insert_game_result(["TEAM1", "20180531", 0.78, 3.51, 2.78, 1.77], DBManager.GAME_MODE_TEAM)
dbmanager.insert_game_result(["TEAM2", "20180531", 0.88, 3.31, 2.11, 1.54], DBManager.GAME_MODE_TEAM)
dbmanager.insert_game_result(["TEAM3", "20180531", 0.91, 2.51, 1.38, 1.21], DBManager.GAME_MODE_TEAM)
dbmanager.insert_game_result(["TEAM4", "20180531", 0.56, 3.51, 2.63, 2.01], DBManager.GAME_MODE_TEAM)
dbmanager.insert_game_result(["TEAM5", "20180531", 0.74, 3.11, 2.13, 1.97], DBManager.GAME_MODE_TEAM)
dbmanager.insert_game_result(["TEAM6", "20180531", 0.77, 1.78, 1.08, 0.98], DBManager.GAME_MODE_TEAM)
dbmanager.insert_game_result(["TEAM7", "20180531", 0.31, 4.15, 3.95, 2.36], DBManager.GAME_MODE_TEAM)
dbmanager.insert_game_result(["TEAM8", "20180531", 0.66, 3.31, 2.97, 2.11], DBManager.GAME_MODE_TEAM)
dbmanager.insert_game_result(["TEAM9", "20180531", 0.97, 2.11, 1.87, 1.54], DBManager.GAME_MODE_TEAM)'''

def team_invite_publish(phone_number) :
    global mqtt_client
    global is_invite_ok
    if is_invite_ok : return
    
    mqtt_client.publish(phone_number + "/RES_TEAM_INVITE", "INVITE", qos=2)
    print("<Server> -", phone_number + "/RES_TEAM_INVITE")
    
    invite_timer = threading.Timer(3, team_invite_publish, args=[phone_number])
    invite_timer.start()

def result_publish(phone_number, result, num) :
    global mqtt_client
    global is_result_ok
    if len(is_result_ok) is num : return
    
    mqtt_client.publish(phone_number + "/RES_SHOW_GAME_RESULT", result, qos=2)
    print("<Server> -", phone_number + "/RES_SHOW_GAME_RESULT", result)
    
    result_timer = threading.Timer(3, result_publish, args=[phone_number, result, num])
    result_timer.start()
    
def initMQTT(host="192.168.0.30", port=1883, keepalive=60):
    global mqtt_client 
    # callback functions setting
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect
    #mqttc.on_subscribe = on_subscribe
    print("<Server> -","Host :", host)
    mqtt_client.connect(host, port, keepalive)
    mqtt_client.loop_forever()

    
def on_message(client, userdata, msg) :
    datas = msg.payload.decode('ascii').split("-")
    process(msg.topic, datas)

def game_finish(request) :
    print("<Server> -","Solo game Finish, User :", request)
    mqtt_client.publish(request + RES_MESSAGE[1], "Solo Game Finish!")
    
def on_connect(client, userdata, flags, rc) :
    print("<Server> -","MQTT Client : on_connect")
    for req in REQ_MESSAGE :
        client.subscribe(req)
    
def process(req, datas):
    global mqtt_client
    global server_state
    global is_invite_ok
    global is_result_ok
    
    request = req.split("/")
    print("<Server> -","process :", request, datas)
    
    if request[1] == "REQ_GAME_START" :
        if server_state is STATE_FREE :
            is_result_ok = []
            server_state = STATE_BUSY
            
            if datas[0] == "solo" :
                print("<Server> -","Solo game start, User :", request[0])
                mqtt_client.publish(request[0] + RES_MESSAGE[0], "ACCEPT")
                game = Game(Game.GAME_MODE_SINGLE, 1, request[0])
                game_result = game.run()
                result_publish(request[0], "-".join(list(map(str, game_result))),1)
                dbmanager.insert_game_result(game_result, DBManager.GAME_MODE_SOLO)
                print("<Server> -","Game over!")
                server_state = STATE_FREE
                
            elif datas[0] == "team" :
                
                server_state = STATE_BUSY
                team_name = datas[1]
                team_num = int(datas[2])+1
                team_member = [request[0]]
                for i in range(3, 3 + team_num) :
                    if len(datas[i]) < 3 : continue
                    team_member.append(datas[i])
                
                print("<Server> -","Team game start")
                print("<Server> -","Team name :", team_name)
                print("<Server> -","Team Num :", team_num+1)
                print("<Server> -","Team member :", team_member)
                
                for member in team_member :
                    mqtt_client.publish(member + RES_MESSAGE[0], "ACCEPT")
                    
                game = Game(Game.GAME_MODE_TEAM, team_num, team_name)
                game_result = game.run()
                
                for member in team_member :
                    print(member + RES_MESSAGE[1])
                    result_publish(member, "-".join(list(map(str, (game_result)))), team_num)
                    
                dbmanager.insert_game_result(game_result, DBManager.GAME_MODE_TEAM)
                print("<Server> -","Game over!")
                server_state = STATE_FREE
                
        elif server_state is STATE_BUSY :
            print("<Server> -","Server is busy. Deny request :", request[0])
            mqtt_client.publish(request[0] + RES_MESSAGE[0], "DENY")
            
    elif request[1] == "REQ_TEAM_INVITE" :
        is_invite_ok = False
        team_invite_publish(request[0])
        
    elif request[1] == "INVITE_OK" :
        is_invite_ok = True
        
    elif request[1] == "RESULT_OK" :
        if len(request[0]) < 3 : return
        
        if not request[0] in is_result_ok :
            is_result_ok.append(request[0])
        
    elif request[1] == "REQ_SHOW_RANKING" :
        print("<Server> -","Requst show ranking from :", request[0])
        
        if datas[0] == "solo" :
            ranking = dbmanager.get_ranking_list(DBManager.GAME_MODE_SOLO)
        
        elif datas[0] == "team" :
            ranking = dbmanager.get_ranking_list(DBManager.GAME_MODE_TEAM)
            
        print("<Server> -","result :", request[0] + RES_MESSAGE[2], ranking)
        mqtt_client.publish(request[0] + RES_MESSAGE[2], ranking)        
    
    elif request[1] == "REQ_SHOW_USERINFO" :
        print("<Server> -","Requst show userinfo from :", request[0])
        mqtt_client.publish(request[0] + RES_MESSAGE[3], "User info")
    
    print()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 1))
host = s.getsockname()[0]
initMQTT(host = host)