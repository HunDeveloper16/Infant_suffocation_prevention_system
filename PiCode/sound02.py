import RPi.GPIO as GPIO
import time

def sound():
    GPIO.setmode(GPIO.BCM)
    gpio_pin = 12
    GPIO.setup(gpio_pin, GPIO.OUT)
    

    p = GPIO.PWM(gpio_pin, 100)
    
    for i in range(3):
        p.start(100)
        p.ChangeDutyCycle(90)
        p.ChangeFrequency(440)
        time.sleep(0.5)
        p.stop()
        time.sleep(1)
    GPIO.cleanup()