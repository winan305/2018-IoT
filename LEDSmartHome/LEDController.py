'''
2018 IoT 개론 및 실습 과제
2013136110 전두영
LED 스마트 홈
LED 컨트롤러 소스
'''

import paho.mqtt.client as mqtt
import RPi.GPIO as gpio

# 초록, 노랑, 빨강 LED GPIO 핀 번호
led_pin = [21, 20, 16]

# LED 상태 플래그
LED_FLAG_GREEN, LED_FLAG_YELLOW, LED_FLAG_RED, LED_FLAG_ALL = 0, 1, 2, 3
# LED 플래그들에 대한 출력 문구
LED_FLAGS = ["GREEN LED ON", "YELLOW LED ON", "RED LED ON", "ALL LED ON"]

# mqtt 클라이언트 객체 생성
mqttc = mqtt.Client()

# mqtt서버 접속 시 호출되는 콜백함수
def on_connect(client, userdata, flags, rc) :
    # LED 컨트롤러가 mqtt 서버에 연결되었음을 출력한다.
    print("LED Controller Connected.")

    # LED 제어값을 subscribe 한다.
    client.subscribe("control/led")

    # LED 핀들의 gpio를 세팅한다.
    gpio.setmode(gpio.BCM)
    for pin in led_pin :
        gpio.setup(pin, gpio.OUT)

# subscribe 하는 메세지를 받았을 때 호출되는 콜백함수
def on_message(client, userdata, msg) :
    # 데이터는 바이너리 데이터이다.
    # 아스키 데이터로 디코드하여 저장한다.
    led_flag = int(msg.payload.decode('ascii'))
    # LED를 켜고 끄는 함수에 led 플래그를 전달한다.
    turnOnOffLED(led_flag)

# LED 플래그로부터 LED를 켜고 끄는 함수다.
def turnOnOffLED(led_flag) :
    print("LED Control :", LED_FLAGS[led_flag])
    # 모든 led 핀들에 대해 반복한다.
    for i in range(len(led_pin)) :
        # 모든 LED를 켜는 플래그로 설정되면 모든 LED를 켠다.
        if led_flag == LED_FLAG_ALL :
            gpio.output(led_pin[i], True)
        # i가 LED 플래그가 같다면 리스트에서 i에 해당하는 LED만을 켠다.
        # 리스트에 0,1,2 번지 순으로 녹색, 노란색, 빨간색 LED GPIO핀이 들어있다.
        # 플래그 또한 순서대로 0,1,2 값을 주었다.
        elif i == led_flag :
            gpio.output(led_pin[i], True)
        # 그 외의 경우 LED핀은 켜지 않는다.
        else :
            gpio.output(led_pin[i], False)

# 호스트, 포트, keepalive 를 전달받아 mqtt서버에 연결하고 루프를 시작하는 함수
# 디폴트는 localhost, 1883, 60 이다.
def start_mqtt(host="localhost", port=1883, keepalive=60) :
    # 콜백함수를 등록한다.
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

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
