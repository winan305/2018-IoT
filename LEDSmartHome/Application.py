'''
2018 IoT 개론 및 실습 과제
2013136110 전두영
가상 스마트 홈
어플리케이션 소스
'''

import paho.mqtt.client as mqtt

# subscribe하는 토픽들을 저장한다.
subscribes = {"temp" : "environment/temperature",
              "humi" : "environment/humidity",
              "dist" : "environment/distance"}

# 사람 감지 여부, 온도, 습도를 선언하고 0으로 초기화한다.
distance = -1
temperature = -1
humidity = -1

LED_GREEN, LED_YELLOW, LED_RED, LED_ALL = 0,1,2,3
LED_FLAGS = ["GREEN LED ON", "YELLOW LED ON", "RED LED ON", "ALL LED ON"]

LIMIT_HUMI = 50
LIMIT_TEMP = 30

# mqtt 클라이언트 객체 생성
mqttc = mqtt.Client()

# mqtt서버 접속 시 호출되는 콜백함수
def on_connect(client, userdata, flags, rc):
    # 어플리케이션이 서버에 연결되었음을 출력한다.
    print("Application Connected.")

    # 어플리케이션이 subscribe 하는 제어값들을 등록한다.
    for subscribe in subscribes.values() :
        client.subscribe(subscribe)


# subscribe 하는 메세지를 받았을 때 호출되는 콜백함수
def on_message(client, userdata, msg) :
    # 사람감지, 온도, 습도는 전역으로 선언된 변수를 사용한다.
    global distance
    global temperature
    global humidity

    # 토픽값을 얻어온다.
    topic = msg.topic

    # 데이터를 얻어오고 아스키 형식으로 디코드한다.
    data = float(msg.payload.decode('ascii'))

    if topic == subscribes["dist"] :
        # 사람감지 여부 변수에 값을 저장하고 램프를 컨트롤한다.
        distance = data
        
    elif topic == subscribes["temp"] :
        # 온도 변수에 데이터를 저장한다.
        temperature = data
        
    # 습도에 대한 토픽인 경우
    elif topic == subscribes["humi"] :
        # 습도 변수에 데이터를 저장한다.
        humidity = data
            
    flag = get_LED_flag([distance, temperature, humidity])
    mqttc.publish("control/led", flag)
    print("distance :", distance, end=' ')
    print("[temperature :", temperature, "humidity :", humidity, "(%)")
    print("LED Control :", LED_FLAGS[flag])
    print()
    
def get_LED_flag(datas) :
    dist, temp, humi = datas
    
    if temp > LIMIT_TEMP or humi > LIMIT_HUMI :
        flag = LED_ALL
        
    elif dist >= 50 :
        flag = LED_GREEN
        
    elif dist > 20 :
        flag = LED_YELLOW
        
    else :
        flag = LED_RED
    
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

try :
    # mqtt 클라이언트를 시작하는 함수를 호출한다.
    start_mqtt()
except KeyboardInterrupt:
    gpio.cleanup()

