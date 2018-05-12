# http://ljs93kr.tistory.com/40

# Orange Pin = GPIO
# RED = 5V
# BROWN = GND

import RPi.GPIO as GPIO
import time

pmws = []
motorPins = [13, 18, 5, 6]
loop_cnt = 0

def init() :
    global pmws
    pmws = []
    global morotPins
    GPIO.setmode(GPIO.BCM)
    for motorPin in motorPins :
        GPIO.setup(motorPin, GPIO.OUT)
        pmw = GPIO.PWM(motorPin, 50)
        pmw.start(0)
        pmws.append(pmw)

def finish() :
    global loop_cnt
    for pmw in pmws :
        pmw.stop()
    if loop_cnt < 3:
        init()
    GPIO.cleanup()
    
def loop() :
    cnt = 0
    angle = 0
    global pmw
    
    while cnt < 5:
        if cnt%2 == 0 : angle = 7.5
        else : angle = 12
        for pmw in pmws :
             pmw.ChangeDutyCycle(angle)
        time.sleep(2)
        print(angle, cnt)
        cnt += 1

#GPIO.cleanup()
init()

while True :
    order = int(input())
    if order == 1 : loop()
    elif order == 2 : finish()
        