#!/usr/bin/python
"""
0.4 Amps/phase
0.11 Nm holding torque
0.9 deg step angle - 400 steps
"""
import time
import numpy as np
from multiprocessing import Process, Queue 
import RPi.GPIO as GPIO

class Servo:
    def __init__(self, queue, pin, verbose="False"):
        self.q = queue
        self.servopin = pin
        self.verbose = verbose

    def start(self):
        self.p = Process(target=self.run, args=((self.q),))
        self.p.start()

    def map(self, value):
        """
        Servo running at 50 Hz -> 20 ms per cycle,
        control: high for 1ms to 2ms controls angle
        20*0.05 == 1Ms
        20*0.1 == 2Ms
        dutycycle value is from 0 to 100,
        value from controller is -1 to 1
        """
        # at 0 we want to pulse to be 1.5 Ms -> 0.075 dutycycle

        value = ((value + 1)/2)  # now 0-1
        value = value*(0.1-0.05)+0.05
        # map to 0-100
        return value * 100

    def run(self, queue):
        inp = (0,0,0)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servopin, GPIO.OUT) # step
        self.pwm = GPIO.PWM(self.servopin, 50)

        self.pwm.start(7.5)

        while True:
            try:
                inp = queue.get_nowait()
                if inp[0] == "right":
                    axis = inp[1]
                    self.dc = self.map(axis)
                    self.pwm.ChangeDutyCycle(self.dc)
                    if self.verbose: print "[Servo] Dutycycle changed to ", axis,",", self.dc
            except:
                time.sleep(0.001)
                pass

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(7, GPIO.OUT) # step
    pwm = GPIO.PWM(7, 50)
    pwm.start(0)

    for i in range(10):
        pwm.ChangeDutyCycle(i)
        time.sleep(0.5)

