from RPi import GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(35,GPIO.OUT)
GPIO.output(33,GPIO.HIGH)
GPIO.output(35,GPIO.HIGH)
a=input("Enter First Number:")
b=input("Enter Sec number :")
c=input("Enter Sum: ")
d=a+b
if c==d:
    GPIO.output(33,GPIO.LOW)
    time.sleep(20)
    GPIO.output(33,GPIO.HIGH)
else:
    GPIO.output(35,GPIO.LOW)
    time.sleep(20)
    GPIO.output(35,GPIO.HIGH)