#!/usr/bin/python
"""
0.4 Amps/phase
0.11 Nm holding torque
0.9 deg step angle - 400 steps
"""
import time
import numpy as np
from multiprocessing import Process
import RPi.GPIO as GPIO

class Linear:
    def __init__(self, queue, verbose="False"):
        self.q = queue
        self.verbose = verbose

        self.numsteps = 400
        self.microstep = 16
        self.actual_steps=self.numsteps * self.microstep

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(3, GPIO.OUT) # step
        GPIO.setup(5, GPIO.OUT) # dir
        GPIO.output(3, GPIO.LOW)

        self.position = 0
        self.speed = 0
        self.direction = 0

    def start(self):
        self.p = Process(target=self.run, args=((self.q),))
        self.p.start()

    def run(self, queue):
        inp = (0,0,0)
        while True:
            try:
                inp = queue.get_nowait()
            except:
                time.sleep(0.000001)
                pass

            if inp[0] == "left": # left stick
                axis = inp[1] #x
                self.direction = np.sign(axis)
                self.speed = abs(float(axis))

            if self.speed > 0:
                if self.direction == 1:
                    GPIO.output(5, GPIO.HIGH)
                else:
                    GPIO.output(5, GPIO.LOW)

                self.speed_rpm = self.speed * 500.0
                # FIXME
                self.speed_rpm = 100
                self.num_steps_per_sec=self.speed_rpm*self.actual_steps/60.0
                self.interval = 1.0/self.num_steps_per_sec
                if self.verbose: print "Interval: ", self.interval

                for i in range(10):
                    GPIO.output(3, GPIO.HIGH)
                    time.sleep(self.interval/2.0)
                    GPIO.output(3, GPIO.LOW)
                    time.sleep(self.interval/2.0)

