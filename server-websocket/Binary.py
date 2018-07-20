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

class Binary:
    def __init__(self, queue, pin):
        self.q = queue
        self.pin = pin
        self.state = 0

    def start(self):
        self.p = Process(target=self.run, args=((self.q),))
        self.p.start()

    def run(self, queue):
        inp = (0,0,0)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.pin, GPIO.OUT) # step

        while True:
            try:
                inp = queue.get_nowait()
                print inp
                if inp[0] == "A":
                    self.state = (self.state + 1) % 2
                    print "[Binary] Changed state to", self.state
                    GPIO.output(self.pin, self.state)
            except:
                time.sleep(0.01)
                pass

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(7, GPIO.OUT) # step
    pwm = GPIO.PWM(7, 50)
    pwm.start(0)

    for i in range(10):
        pwm.ChangeDutyCycle(i)
        time.sleep(0.5)

