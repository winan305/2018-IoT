'''
2018-1학기 IoT 개론 및 실습
[개인과제 02] GPIO 프로그래밍 실습
2013136110 전두영
최종 수정일 : 2018-04-07
'''


import RPi.GPIO as gpio
import time
import spidev

# spi모듈 사용을 위해 초기화
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 61000

# 조도 센서 채널값 설정
light_channel = 0

# 초록, 노랑, 빨강 LED GPIO 핀 번호
led_pin = [16, 20, 21]
# LED 상태 플래그
LED_FLAG_GREEN, LED_FLAG_YELLOW, LED_FLAG_RED, LED_FLAG_ALL = 0, 1, 2, 3
# 조도센서의 값이 150보다 작아지면 모든 LED를 켠다.
LIGHT_LIMIT = 150

# 초음파 센서 트리거, 에코핀 GPIO 핀 번호
trig_pin = 13
echo_pin = 19

# 핀 상태 초기화 함수
def initPins() :
    print("Pin init")
    
    gpio.setmode(gpio.BCM)
    gpio.setup(trig_pin, gpio.OUT)
    gpio.setup(echo_pin, gpio.IN)
    gpio.setwarnings(False)
    
    for pin in led_pin :
        gpio.setup(pin, gpio.OUT)

# 채널로부터 아날로그 값 얻기
def readChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((adc[1] & 3) << 8) + adc[2]
    return adc_out

# 조도 센서로부터 빛의 세기를 읽어와 반환하는 함수
def getLightValue() :
    # 조도센서 값을 얻는다.
    light_level = readChannel(light_channel)
    # 빛의 세기를 반환한다.
    return light_level

# 초음파 센서로부터 물체와의 거리를 반환하는 함수
def getUltraValue() :
    # 트리거 핀의 출력에 변화를 준다.
    gpio.output(trig_pin, False)
    time.sleep(0.5)
    
    gpio.output(trig_pin, True)
    time.sleep(0.00001)
    gpio.output(trig_pin, False)

    # 에코핀의 입력값이 0이면 시간측정을 시작한다.
    while gpio.input(echo_pin) == 0:
        pulse_start = time.time()

    # 에코핀의 입력값이 1이면 시간측정을 종료한다.
    while gpio.input(echo_pin) == 1:
        pulse_end = time.time()

    # 종료시간 - 시작시간으로 초음파의 왕복 시간을 구한다.
    pulse_duration = pulse_end - pulse_start
    # 수식을 통해 거리를 계산하고 2자리까지 반올림한다.
    distance = pulse_duration * 34000 / 2
    distance = round(distance, 2)

    # 거리를 반환한다.
    return distance

# 초음파에서 얻은 물체와의 거리, 조도센서에서 얻은 빛의 세기를 기준으로
# LED의 플래그를 설정하고 반환하는 함수다.
def getLEDFlag(distance, light_level) :
    # 빛의 세기가 한계치보다 작으면 모든 LED를 켜는 플래그로 설정한다.
    if light_level < LIGHT_LIMIT :
        led_flag = LED_FLAG_ALL
        print("All LED On!!")
    if light_level > 550 :
        print("Laser!!")
        led_flag = LED_FLAG_GREEN

    # 물체와의 거리가 30cm 이상이면 녹색 LED를 켜는 플래그로 설정한다.
    elif distance >= 30 :
        led_flag = LED_FLAG_GREEN
        print("Green LED On!")

    # 물체와의 거리가 10센치보다 크면 노란색 LED를 켜는 플래그로 설정한다.
    elif distance > 10 :
        led_flag = LED_FLAG_YELLOW
        print("Yellow LED On!")

    # 10cm 이하이면 빨간 LED를 켜는 플래그로 설정한다.
    else :
        led_flag = LED_FLAG_RED
        print("Red LED On!")

    # 설정된 led 플래그를 반환한다.
    return led_flag

# LED 플래그로부터 LED를 켜고 끄는 함수다.
def turnOnOffLED(led_flag) :
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

#위 함수들을 적절히 호출하여 프로그램을 실행하는 main 함수다.
def main() :
    # 핀들을 초기화한다.
    initPins()
    # 키보드 인터럽트가 발생하지 않으면 try 내부의 코드를 실행한다.
    try:
        # Main이 시작됨을 출력한다.
        print("Main Start.")

        # 무한 반복한다.
        while True:
            # 반복 간 한줄 띄워 읽기 쉽게 하기위해 삽입한 print문이다.
            print()
            # 거리와 빛의 세기값을 얻어온다.
            distance = getUltraValue()
            light_level = getLightValue()

            # 거리와 빛의 세기를 출력한다.
            print("Light: ", light_level)
            print("Distance : ", distance, "cm")

            # LED 플래그를 얻어와 LED를 켠다.
            # turnOnOffLED 함수 내부에서 어떤 LED를 켜는지 출력한다.
            led_flag = getLEDFlag(distance, light_level)
            turnOnOffLED(led_flag)

            # 1ms 쉰다.
            time.sleep(0.1)

    # 키보드 인터럽트 예외 발생 시 예외처리한다.
    # spi를 닫고 gpio를 클린하고 프로그램을 종료하게 된다.
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Program Finish..")
        spi.close()
        gpio.cleanup()

# 메인함수를 호출하여 프로그램을 실행한다.
main()