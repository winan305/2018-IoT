
'''
2018 IoT 개론 및 실습 과제
2013136110 전두영
LED 스마트 홈
초음파 센서 코드
'''

import paho.mqtt.client as mqtt
from random import *
import threading
import RPi.GPIO as gpio
import time
import spidev

trig_pin = 13
echo_pin = 19

gpio.setmode(gpio.BCM)
gpio.setup(trig_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)

# 메시지를 publish 하는 시간 간격(초)
PUBLISHING_TIME = 1

# mqtt 클라이언트 객체 생성
mqttc = mqtt.Client()
    
# mqtt서버 접속 시 호출되는 콜백함수
def on_connect(client, userdata, flags, rc) :
    # 초음파 센서가 mqtt 서버에 연결되었음을 출력한다.
    print("Ultra Sensor Connected.")
    # 초음파 센서로부터 데이터를 읽어 publish한다.
    publish(read_data())

# 초음파 센서로부터 1회 데이터를 읽어 반환하는 함수
def read_data() :
    # 트리거핀에 변화를 준다.
    gpio.output(trig_pin, False)
        
    gpio.output(trig_pin, True)
    time.sleep(0.00001)
    gpio.output(trig_pin, False)

    # 에코핀으로 부터 초음파가 나갔다가 돌아오는 시간을 측정한다.
    while gpio.input(echo_pin) == 0:
        pulse_start = time.time()
            
    while gpio.input(echo_pin) == 1:
        pulse_end = time.time()

    # 초음파의 왕복 시간으로부터 거리를 구한다.
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34000 / 2
    # 소수 2번째자리까지 반올림한다.
    distance = round(distance, 2)

    # 거리 데이터를 반환한다.
    return distance

# 데이터를 전달받아 서버에 publish 하는 함수
def publish(data) :
    # 거리 데이터를 publish 하고 데이터를 출력한다.
    mqttc.publish("environment/distance", data)
    print("Distance :", data)
    
    # 타이머를 생성하여 PUBLISHING_TIME초(1초) 뒤에 data를 매개변수로 하여 함수를 호출한다.
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

