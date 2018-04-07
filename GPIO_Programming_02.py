import RPi.GPIO as gpio
import time
import spidev

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 61000

light_channel = 0
temp_channel = 1

led_pin = [16, 20, 24]
LED_FLAG_GREEN, LED_FLAG_YELLOW, LED_FLAG_RED, LED_FLAG_ALL = 0, 1, 2, 3
LIGHT_LIMIT = 150

trig_pin = 13
echo_pin = 19

def initPins() :
    print("Pin init")
    
    gpio.setmode(gpio.BCM)
    gpio.setup(trig_pin, gpio.OUT)
    gpio.setup(echo_pin, gpio.IN)
    gpio.setwarnings(False)
    
    for pin in led_pin :
        gpio.setup(pin, gpio.OUT)
    
def readChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((adc[1] & 3) << 8) + adc[2]
    return adc_out
	
def convert2volts(data, places):
    volts = (data * 3.3) / float(1023)
    volts = round(volts, places)
    return volts

def convert2temp(data, places):
    temp = ((data * 330) / float(1023)) - 50
    temp = round(temp, places)
    return temp
	
def getLightValue() :
    light_level = readChannel(light_channel)
    light_volts = convert2volts(light_level, 2)
    
    temp_level = readChannel(temp_channel)
    temp_volts = convert2volts(temp_level, 2)
    temp = convert2temp(temp_level, 2)
    
    return light_level

def getUltraValue() :
    gpio.output(trig_pin, False)
    time.sleep(0.5)
    
    gpio.output(trig_pin, True)
    time.sleep(0.00001)
    gpio.output(trig_pin, False)
    
    while gpio.input(echo_pin) == 0:
        pulse_start = time.time()
        
    while gpio.input(echo_pin) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34000 / 2
    distance = round(distance, 2)
    
    return distance

def getLEDState(distance, light_level) :
    led_state = None
    
    if light_level < LIGHT_LIMIT :
        led_state = LED_FLAG_ALL
        print("All LED On!!")
        
    elif distance >= 30 :
        led_state = LED_FLAG_GREEN
        print("Green LED On!")
    
    elif distance > 10 :
        led_state = LED_FLAG_YELLOW
        print("Yellow LED On!")
    
    else :
        led_state = LED_FLAG_RED
        print("Red LED On!")
    
    return led_state

def turnOnOffLED(led_state) :
    if led_state == None : return
    
    for i in range(len(led_pin)) :
        if led_state == LED_FLAG_ALL :
            gpio.output(led_pin[i], True)
            
        elif i == led_state :
            gpio.output(led_pin[i], True)
            
        else :
            gpio.output(led_pin[i], False)
            
def main() :
    initPins()
    try:
        print("Main Start.")
        while True:
            distance = getUltraValue()
            light_level = getLightValue()
            
            print("Light: ", light_level)
            print("Distance : ", distance, "cm")
            print()
            
            led_state = getLEDState(distance, light_level)
            turnOnOffLED(led_state)
            
            time.sleep(1)
            
    except KeyboardInterrupt as e:
        print("Keyboard Interrupt. Program Finish..")
        spi.close()
        gpio.cleanup()
        
main()