'''
2018 IoT 개론 및 실습 과제
2013136110 전두영
LED 스마트 홈
어플리케이션 소스
'''

import paho.mqtt.client as mqtt

# subscribe하는 토픽들을 딕셔너리에 키:값 쌍으로 저장한다.
subscribes = {"temp" : "environment/temperature",
              "humi" : "environment/humidity",
              "dist" : "environment/distance"}

# 거리, 온도, 습도 데이터값을 -1로 초기화한다.
distance = -1
temperature = -1
humidity = -1

# LED 상태 플래그
LED_GREEN, LED_YELLOW, LED_RED, LED_ALL = 0,1,2,3
# LED 플래그들에 대한 출력 문구
LED_FLAGS = ["GREEN LED ON", "YELLOW LED ON", "RED LED ON", "ALL LED ON"]

<<<<<<< HEAD
LIMIT_HUMI = 50
LIMIT_TEMP = 30
=======
# 온습도 센서의 제한값. 이 값을 넘으면 모든 LED를 켠다.
LIMIT_HUMI = 123
LIMIT_TEMP = 9876543210
>>>>>>> bd10173105257b3a8eaf7f0736963d7dc39b2ce8

# mqtt 클라이언트 객체 생성
mqttc = mqtt.Client()

# mqtt서버 접속 시 호출되는 콜백함수
def on_connect(client, userdata, flags, rc):
    # 어플리케이션이 서버에 연결되었음을 출력한다.
    print("Application Connected.")

    # 어플리케이션이 subscribe 하는 토픽들을 등록한다.
    for subscribe in subscribes.values() :
        client.subscribe(subscribe)

# subscribe 하는 메세지를 받았을 때 호출되는 콜백함수
def on_message(client, userdata, msg) :
    # 거리, 온도, 습도는 전역으로 선언된 변수를 사용한다.
    global distance
    global temperature
    global humidity

    # 토픽값을 얻어온다.
    topic = msg.topic

    # 데이터를 얻어오고 아스키 형식으로 디코드한다.
    data = float(msg.payload.decode('ascii'))

    # 토픽이 거리인 경우
    if topic == subscribes["dist"] :
        # 거리변수에 저장한다.
        distance = data

    # 토픽이 온도인 경우
    elif topic == subscribes["temp"] :
        # 온도 변수에 데이터를 저장한다.
        temperature = data
        
    # 토픽이 습도인 경우
    elif topic == subscribes["humi"] :
        # 습도 변수에 데이터를 저장한다.
        humidity = data

    # [거리, 온도, 습도] 리스트로부터 알맞은 led 플래그를 반환하는 함수로부터 flag를 얻는다.
    flag = get_LED_flag([distance, temperature, humidity])
    # 얻은 플래그를 publish 한다.
    mqttc.publish("control/led", flag)
    # 거리, 온도, 습도를 출력하고 LED 제어에 대한 문구를 출력한다.
    print("distance :", distance, end=' ')
    print("[temperature :", temperature, "humidity :", humidity, "(%)")
    print("LED Control :", LED_FLAGS[flag])
    print()

# 데이터들로부터 led 제어 플래그를 반환하는 함수
def get_LED_flag(datas) :
    # [거리, 온도, 습도] 데이터 리스트이므로 저장해준다.
    dist, temp, humi = datas

    # 온도 혹은 습도가 제한값을 넘으면 모든 led를 켜는 플래그를 저장한다.
    if temp > LIMIT_TEMP or humi > LIMIT_HUMI :
        flag = LED_ALL

    # 그 외의 경우는 거리값에 따라 led 플래그를 저장한다.
    elif dist >= 50 :
        flag = LED_GREEN
        
    elif dist > 20 :
        flag = LED_YELLOW
        
    else :
        flag = LED_RED

    # 결정된 플래그를 반환한다.
    return flag

# 호스트, 포트,  keepalive 를 전달받아 mqtt서버에 연결하고 루프를 시작하는 함수
# 디폴트는 localhost, 1883, 60 이다.
def start_mqtt(host="localhost", port=1883,  keepalive=60) :
    # 콜백함수를 등록한다.
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    # 호스트와 포트번호를 가진 mqtt 서버에 접속한다.
    mqttc.connect(host, port,  keepalive)

    # 루프를 실행한다.
    mqttc.loop_forever()

# mqtt 클라이언트를 시작하는 함수를 호출한다.
start_mqtt()


