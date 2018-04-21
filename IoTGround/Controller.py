import RPi.GPIO as GPIO
import time
import spidev

class Controller :
    '''
    컨트롤러 클래스
    조도센서 8개, 서보모터 4개
    '''
    
    INIT_REPEAT = 5
    TARGET_NUMBER = 4
    FLAG_TARGET_UP, FLAG_TARGET_DOWN = 0 , 1
    TARGET_STATE = [False] * TARGET_NUMBER
    TARGET_UP_ANGLE, TARGET_DOWN_ANGLE = 7.5, 12
    # GPIO 5, 6, 13, 19 사용
    motorPins = [18, 5,6,13]
    pmws = []

    LIGHT_SENSOR_NUMBER = 8
    light_channels = [i for i in range(LIGHT_SENSOR_NUMBER)]
    AVG_LIGHT_VALUE = [0] * LIGHT_SENSOR_NUMBER

    def __init__(self):
        '''
        생성자 함수.
        여기서 핀모드를 설정하든 뭘 하든 하면 되겠지?
        '''
        print("Log : Controller Class Object init")
        # 여기서부터 모터

        GPIO.setmode(GPIO.BCM)

        # 여기서부터 조도센서 spi모듈 사용을 위해 초기화
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 61000

    def readChannel(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        adc_out = ((adc[1] & 3) << 8) + adc[2]
        return adc_out

    def getLigthValue(self, channel) :
        '''
        조도센서로부터 값을 얻는 함수
        :param wait: 반복간 얼마나 기다리면서 측정할 것인가? 기본 0초
        :param repeat: 얼마나 반복할 것인가? 기본 1회
        :return: 조도센서 값 리턴
        '''
        light_level = self.readChannel(channel)
        return light_level

    def controllTarget(self, number, flag) :
        '''
        서보모터 번호와 각도를 입력받아서 돌림(과녁을 눕히고 세움)
        :param number: 서보모터(타겟) 번호(1번 과녁, 2번과녁 이렇게 되겠지.)
        :param flag: 눕힐래 세울래? 90도냐 -90도냐는 고정이고.
        :return:
        '''
        if flag == self.FLAG_TARGET_UP :
            self.pmws[number].ChangeDutyCycle(self.TARGET_UP_ANGLE)

        elif flag == self.FLAG_TARGET_DOWN :
            self.pmws[number].ChangeDutyCycle(self.TARGET_DOWN_ANGLE)


    def getLightSensorState(self, channel) :
        light_value = self.getLigthValue(channel)
        return light_value > self.AVG_LIGHT_VALUE[channel] + 100

    def initSensorState(self) :
        '''
        센서 초기상태를 설정하는 함수. 그래봐야 조도센서 뿐이겠지.
        현재 장소의 평균 조도센서 값을 저장함
        why?
        장소, 계절, 조명상태마다 조도센서 값이 달라짐
        달라지는 그 값을 기준으로 레이저를 받았을 때 값차이가 피격의 기준이 되야함
        그래야 어느곳에서든 할 수 있다.

        how?
        처음 게임이 실행되면 이 함수를 호출함
        조도센서로부터 값을 5회정도 받아서 평균내면 되지 않을까?
        '''
        self.start()
        
        # 모든 표적지를 세움
        for pmw in self.pmws :
            pmw.ChangeDutyCycle(self.TARGET_UP_ANGLE)

        for _ in range(self.INIT_REPEAT) :
            for light_channel in self.light_channels :
                self.AVG_LIGHT_VALUE[light_channel] += self.getLigthValue(light_channel)
            time.sleep(0.5)

        for i in self.light_channels :
            self.AVG_LIGHT_VALUE[i] = int(self.AVG_LIGHT_VALUE[i] / 5)

        # 모든 표적지를 눕힘
        for pmw in self.pmws :
            pmw.ChangeDutyCycle(self.TARGET_DOWN_ANGLE)

        print("Log : Call initSensorState(), result =", self.AVG_LIGHT_VALUE)
        
    def start(self) :
        for motorPin in self.motorPins :
            GPIO.setup(motorPin, GPIO.OUT)
            p = GPIO.PWM(motorPin, 50)
            p.start(0)
            self.pmws.append(p)

    def stop(self) :
        for pmw in self.pmws :
            pmw.stop()