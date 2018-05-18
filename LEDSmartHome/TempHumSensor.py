'''
2018 IoT 개론 및 실습 과제
2013136110 전두영
LED 스마트 홈
온습도 센서 소스
'''

import paho.mqtt.client as mqtt
from random import *
import threading
import RPi.GPIO as gpio
import dht11
import time
import datetime

# GPIO 핀을 초기화한다.
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.cleanup()

# 온습도 센서핀 5번으로 부터 인스턴스를 얻는다.
instance = dht11.DHT11(pin = 5)

# 메시지를 publish 하는 시간 간격(초)
PUBLISHING_TIME = 2

# mqtt 클라이언트 객체 생성
mqttc = mqtt.Client()

# mqtt서버 접속 시 호출되는 콜백함수
def on_connect(client, userdata, flags, rc) :
    # 온도/습도 센서가 mqtt 서버에 연결되었음을 출력한다.
    print("Temperature/Humidity Sensor Connected.")
    # 온습도 센서값을 읽어들여 publish 한다.
    publish(read_data())

# 온습도 센서값이 유효한 경우 반환하는 함수, 유효하지 않다면 -1을 반환한다.
def read_data() :
    # 인스턴스로부터 결과데이터를 읽는다.
    result = instance.read()
    # 유효하다면 튜플로 (온도, 습도)를 반환하고 유효하지 않다면 -1을 반환한다.
    return (result.temperature, result.humidity) if result.is_valid() else -1

# 데이터를 전달받아 서버에 publish 하는 함수
def publish(data) :
    # 데이터가 -1인 경우 publish 하지 않고 유효하지 않음을 출력한다.
    if data is -1 :
        print("Sensor Data is not valid.")

    # 데이터가 유효한 경우
    else :
        # data는 (온도, 습도) 튜플이므로 저장해준다.
        temp, humi = data

        # 온도와 습도를 해당 토픽으로 하여 publish 한다.
        mqttc.publish("environment/temperature", temp)
        mqttc.publish("environment/humidity", humi)
    
        # 생성된 값들을 출력하고 튜플로 반환한다.
        print("온도 :", temp, ", 습도 :", humi, "(%)")
    
    # 타이머를 생성하여 PUBLISHING_TIME초(2초) 뒤에 data를 매개변수로 하여 함수를 호출한다.
    # 타이머를 시작하면 2초뒤에 타이머가 실행된다.
    # 타이머가 publish 함수를 호출하므로 2초마다 무한 반복된다.
    publish_timer = threading.Timer(PUBLISHING_TIME, publish, args=[read_data()])
    publish_timer.start()

# 호스트, 포트, keepalive 를 전달받아 mqtt서버에 연결하고 루프를 시작하는 함수
# 디폴트는 localhost, 1883, 60 이다.
def start_mqtt(host="localhost", port=1883, keepalive=60) :
    # 콜백함수를 등록한다.
    mqttc.on_connect = on_connect

    # 호스트와 포트번호를 가진 mqtt 서버에 접속한다.
    mqttc.connect(host, port, keepalive)

    # 루프를 실행한다.
    mqttc.loop_forever()

# 키보드 인터럽트가 발생하면 gpio핀을 클린업 한다.
try :
    # mqtt 클라이언트를 시작하는 함수를 호출한다.
    start_mqtt()
except KeyboardInterrupt:
    gpio.cleanup()


