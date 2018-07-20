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
    def __init__(self, queue):
        self.q = queue
        self.position = 0


    def start(self):
        self.p = Process(target=self.run, args=((self.q),))
        self.p.start()

    def run(self, queue):
        inp = (0,0,0)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(7, GPIO.OUT) # step
        self.pwm = GPIO.PWM(7, 50)

        self.pwm.start(2.5)

        while True:
            try:
                inp = queue.get_nowait()
                if inp[0] == "right":
                    axis = inp[1]
                    self.position = float(axis)
                    if self.position > 0:
                        self.dc = 12.5
                    else:
                        self.dc = 5
                    """
                    self.dc = max(0, min(100, abs(float(axis)*100.0)))
                    """
                    self.pwm.ChangeDutyCycle(self.dc)
                    print "[Servo] Dutycycle changed to ", self.dc
            except:
                pass

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(7, GPIO.OUT) # step
    pwm = GPIO.PWM(7, 50)
    pwm.start(0)

    for i in range(10):
        pwm.ChangeDutyCycle(i)
        time.sleep(0.5)

