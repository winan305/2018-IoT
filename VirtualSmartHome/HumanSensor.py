'''
2018 IoT 개론 및 실습 과제
2013136110 전두영
가상 스마트 홈
사람감지 센서 코드
'''

import paho.mqtt.client as mqtt
from random import *
import threading

# 메시지를 publish 하는 시간 간격(초)
PUBLISHING_TIME = 2

# mqtt 클라이언트 객체 생성
mqttc = mqtt.Client()

# mqtt서버 접속 시 호출되는 콜백함수
def on_connect(client, userdata, flags, rc):
    # 휴먼 센서가 mqtt 서버에 연결되었음을 출력
    print("Human Sensor Connected.")
    # 랜덤 데이터를 생성하여 publish 한다.
    publish(generate_data())

# 랜덤으로 데이터를 발생시키는 함수
def generate_data():
    # 0,1 데이터 생성, 사람이 있는지 없는지에 대한 값이다.
    isPerson = randrange(2)
    # 1이면 사람이 감지, 아니라면 감지가 안됨을 출력한다.
    print("사람 감지됨" if isPerson is 1 else "사람 감지 안됨")
    # 감지 데이터 반환
    return isPerson

# 데이터를 전달받아 서버에 publish 하는 함수
def publish(data):
    # 타이머를 생성하여 PUBLISHING_TIME초(2초) 뒤에 data를 매개변수로 하여 함수를 호출한다.
    publish_timer = threading.Timer(PUBLISHING_TIME, publish, args=generate_data())
    # 함수 호출 시 data를 서버에 publish 한다.
    # 인체감지 센서이므로 해당 토픽은 home/person 이다.
    mqttc.publish("home/person", data)
    # 타이머를 시작하면 2초뒤에 타이머가 실행된다.
    # 타이머가 publish 함수를 호출하므로 2초마다 무한 반복된다.
    publish_timer.start()

# 호스트, 포트, keepalive 를 전달받아 mqtt서버에 연결하고 루프를 시작하는 함수
# 디폴트는 localhost, 1883, 60 이다.
def start_mqtt(host="localhost", port=1883, keepalive=60) :
    # 콜백함수를 등록한다.
    mqttc.on_connect = on_connect

    # 호스트와 포트번호를 가진 mqtt 서버에 접속한다.
    mqttc.connect(host, port, keepalive)

    # 루프를 실행한다.
    mqttc.loop_start()

# mqtt 클라이언트를 시작하는 함수를 호출한다.
start_mqtt()

