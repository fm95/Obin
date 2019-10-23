from thethings.thethingsAPI import ThethingsAPI
from random import randrange
import RPi.GPIO as GPIO
import time
import requests
import ttrest
import ttn

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#set GPIO Pins
GPIO_TRIGGER = 36
GPIO_ECHO = 38

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

red = 7
GPIO.setup(red, GPIO.OUT)
green = 32
GPIO.setup(green, GPIO.OUT)

### FUNCTIONS ####################################

def distance():
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)
    time.sleep(0.1)

    GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)

    GPIO.output(GPIO_TRIGGER, GPIO.LOW)

    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2

    print "Calculating distance ..." 
    return distance

def blink(col):
    GPIO.output(col, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(col, GPIO.LOW)


###################################################

if __name__ == '__main__':
    try:
        while True:
            dist = distance()

            # bin: 30 * 41.2 cm 
            if dist < 0:
                dist = 0
            elif dist > 40:
                dist = 41.5

            # Percentage calculation
            # dist : 50 = x : 100
            perc = (dist * 100) / 41.5
	        level = 100 - perc

            ### WEBAPP ###
            #thethings = ThethingsAPI("wp3N1f_XKyMGeZXv0y4fJW2rqXm8MbYohzbnuPjEKaw")
            #thethings.addVar("percentage", str(percentage))
            #thethings.write()

            # LED
            if level < 50:
                blink(green)
            #elif level < 70:
            #    blink(red)
            else:
                blink(red)

            # Console
            print ("Measured Distance = %.1f cm" % dist)
            print ("Garbage level = %.1f percent \n \n" % level)

            # Update-time
            time.sleep(1)
 

    # wrong distance value
    except Exception:
        GPIO.cleanup()

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

































