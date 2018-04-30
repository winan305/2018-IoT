'''
2018 IoT 개론 및 실습 과제
2013136110 전두영
가상 스마트 홈
온/습도 센서 코드
'''

import paho.mqtt.client as mqtt
from random import *
import threading


# 메시지를 publish 하는 시간 간격(초)
PUBLISHING_TIME = 2

# mqtt 클라이언트 객체 생성
mqttc = mqtt.Client()

# mqtt서버 접속 시 호출되는 콜백함수
def on_connect(client, userdata, flags, rc) :
    # 온도/습도 센서가 mqtt 서버에 연결되었음을 출력한다.
    print("Temperature/Humidity Sensor Connected.")
    # 랜덤 데이터를 생성하여 publish 한다.
    publish(generate_data())

# 랜덤으로 데이터를 발생시키는 함수
def generate_data() :
    # 15~35 사이의 온도값을 임의로 생성한다.
    temp = randrange(15, 36)
    # 30~95(%) 사이의 흡도값을 임의로 생성한다.
    # 정수로 발생된 30~95 사이의 값을 100으로 나누고 두번째 자리까지 반올림한다.
    humi = round((randrange(30, 96) / 100), 2)

    # 생성된 값들을 출력하고 튜플로 반환한다.
    print("온도 :", temp, ", 습도 :", humi)
    return (temp, humi)

# 데이터를 전달받아 서버에 publish 하는 함수
def publish(data) :
    # 타이머를 생성하여 PUBLISHING_TIME초(2초) 뒤에 data를 매개변수로 하여 함수를 호출한다.
    publish_timer = threading.Timer(PUBLISHING_TIME, publish, args=generate_data())

    # data는 (온도, 습도) 튜플이므로 저장해준다.
    temp, humi = data

    # 온도와 습도를 해당 토픽으로 하여 publish 한다.
    mqttc.publish("home/temperature", temp)
    mqttc.publish("home/humidity", humi)

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
