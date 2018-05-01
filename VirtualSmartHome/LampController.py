'''
2018 IoT 개론 및 실습 과제
2013136110 전두영
가상 스마트 홈
전등 컨트롤러 소스
'''

import paho.mqtt.client as mqtt

# mqtt 클라이언트 객체 생성
mqttc = mqtt.Client()

# mqtt서버 접속 시 호출되는 콜백함수
def on_connect(client, userdata, flags, rc) :
    # 전등 컨트롤러가 mqtt 서버에 연결되었음을 출력한다.
    print("Lamp Controller Connected.")

    # 전등 제어값을 subscribe 한다.
    client.subscribe("home/controll/lamp")

# subscribe 하는 메세지를 받았을 때 호출되는 콜백함수
def on_message(client, userdata, msg) :
    # 데이터는 바이너리 데이터이다.
    # 아스키 데이터로 디코드하여 저장한다.
    data = msg.payload.decode('ascii')

    # 에어컨 컨트롤 함수에 데이터를 전달한다.
    controll(data)

# 제어 메세지를 전달받아 에어컨을 컨트롤하는 함수
def controll(controll_msg) :
    # 제어 메세지가 ON 이면 전등을 켠다.
    if controll_msg == "ON" :
        print("Light ON")

    # 제어 메세지가 OFF 이면 전등을 끈다.
    elif controll_msg == "OFF" :
        print("Light OFF")

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

# mqtt 클라이언트를 시작하는 함수를 호출한다.
start_mqtt()

