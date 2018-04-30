'''
2018 IoT 개론 및 실습 과제
2013136110 전두영
가상 스마트 홈
어플리케이션 소스
'''

import paho.mqtt.client as mqtt

# subscribe하는 토픽들을 저장한다.
sub_temp = "home/temperature"
sub_humi = "home/humidity"
sub_person = "home/person"

# 사람 감지 여부, 온도, 습도를 선언하고 0으로 초기화한다.
isPerson = 0
temperature = 0
humidity = 0

# mqtt 클라이언트 객체 생성
mqttc = mqtt.Client()

# mqtt서버 접속 시 호출되는 콜백함수
def on_connect(client, userdata, flags, rc):
    # 어플리케이션이 서버에 연결되었음을 출력한다.
    print("Application Connected.")

    # 어플리케이션이 subscribe 하는 제어값들을 등록한다.
    client.subscribe(sub_temp)
    client.subscribe(sub_humi)
    client.subscribe(sub_person)

# subscribe 하는 메세지를 받았을 때 호출되는 콜백함수
def on_message(client, userdata, msg) :
    # 사람감지, 온도, 습도는 전역으로 선언된 변수를 사용한다.
    global isPerson
    global temperature
    global humidity

    # 토픽값을 얻어온다.
    topic = msg.topic

    # 데이터를 얻어오고 아스키 형식으로 디코드한다.
    data = msg.payload.decode('ascii')

    # 토픽이 사람감지에 대한 토픽인 경우
    if topic == sub_person :
        # 사람감지 여부 변수에 값을 저장하고 램프를 컨트롤한다.
        isPerson = data
        controll_lamp(isPerson)

    # 그 외의 토픽인 경우
    else :
        # 온도에 대한 토픽인 경우
        if topic == sub_temp :
            # 온도 변수에 데이터를 저장한다.
            temperature = data

        # 습도에 대한 토픽인 경우
        elif topic == sub_humi :
            # 습도 변수에 데이터를 저장한다.
            humidity = data

        # 저장된 온도와 습도로 에어컨을 컨트롤한다.
        controll_aircon(temperature, humidity)

# 사람감지 여부를 전달받아 램프를 컨트롤하는 메세지를 publish 하는 함수
def controll_lamp(isPerson) :

    # 사람이 감지되면 램프 ON 제어 메세지를 publish 한다.
    if isPerson is 1 :
        mqttc.publish("home/controll/lamp", "ON")

    # 사람이 감지되지 않으면 램프 OFF 제어 메세지를 publish 한다.
    else :
        mqttc.publish("home/controll/lamp", "OFF")

# 기온과 상대습도를 전달받고 불쾌지수를 얻어 에어컨 제어 메시지를 publish 하는 함수
def controll_aircon(T, RH) :
    # T = 기온, RH = 상대습도
    # 상대습도 계산식에 따라 불쾌지수를 계산한다.
    discomfort_index = (9/5)*T - 0.55*(1-RH)*((9/5)*T-26) + 32

    # 불쾌지수 레벨을 얻어온다.
    level = get_level(discomfort_index)

    # 불쾌지수에 따라 에어컨 제어 메시지를 얻는 딕셔너리
    # {키 : 값} = {불쾌지수 : 제어메세지}
    controll_dict = {"Very High" : "START", "High" : "START", "Low" : "STOP"}

    # 사람이 없다면 불쾌지수와 관계없이 에어컨 STOP 메세지를 publish 한다.
    if isPerson is 0 :
        mqttc.publish("home/controll/aircon", "STOP")

    # 사람이 있다면 불쾌지수에 따라 제어메세지를 publish 한다.
    else :
        mqttc.publish("home/controll/aircon", controll_dict[level])

    # 불쾌지수 값, 단계, 온도, 습도(%)를 출력한다.
    print(round(discomfort_index,2), "(" + level + ")", "[temperature :", T, "humidity :", RH, "(%)")

# 불쾌지수의 값에 따라 단계를 반환하는 함수
def get_level(discomfort_index) :
    # 기준에 다라 Very High, High, Normal, Low 를 가지며, 이를 반환한다.
    if discomfort_index >= 80 :
        level = "Very High"
    elif discomfort_index >= 75 :
        level = "High"
    elif discomfort_index >= 68 :
        level = "Normal"
    else :
        level = "Low"
    return level

# 호스트, 포트,  keepalive 를 전달받아 mqtt서버에 연결하고 루프를 시작하는 함수
# 디폴트는 localhost, 1883, 60 이다.
def start_mqtt(host="localhost", port=1883,  keepalive=60) :
    # 콜백함수를 등록한다.
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    # 호스트와 포트번호를 가진 mqtt 서버에 접속한다.
    mqttc.connect(host, port,  keepalive)

    # 루프를 실행한다.
    mqttc.loop_start()

# mqtt 클라이언트를 시작하는 함수를 호출한다.
start_mqtt()

