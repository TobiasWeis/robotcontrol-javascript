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

class Linear:
    def __init__(self, queue):
        self.q = queue
        self.numsteps = 400
        self.microstep = 16
        self.actual_steps=self.numsteps * self.microstep

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(3, GPIO.OUT) # step
        GPIO.setup(5, GPIO.OUT) # dir
        GPIO.output(3, GPIO.LOW)

        self.position = 0

    def start(self):
        self.p = Process(target=self.run, args=((self.q),))
        self.p.start()

    def run(self, queue):
        axis = 0
        while True:
            try:
                axis = queue.get_nowait()
            except:
                pass
            #print "[Linear] Got axis-value: ", axis

            direction = np.sign(axis)
            speed = abs(float(axis))

            if speed > 0:
                if direction == 1:
                    GPIO.output(5, GPIO.HIGH)
                else:
                    GPIO.output(5, GPIO.LOW)

                self.speed_rpm = speed * 500.0
                # FIXME
                self.speed_rpm = 100
                self.num_steps_per_sec=self.speed_rpm*self.actual_steps/60.0
                self.interval = 1.0/self.num_steps_per_sec
                print "Interval: ", self.interval

                for i in range(10):
                    GPIO.output(3, GPIO.HIGH)
                    time.sleep(self.interval/2.0)
                    GPIO.output(3, GPIO.LOW)
                    time.sleep(self.interval/2.0)


"""
for j in range(100):
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(3, GPIO.LOW)

    print "Performing ",ACTUAL_STEPS, " steps with interval ", INTERVAL

    # try to do several steps
    for i in range(ACTUAL_STEPS):
        GPIO.output(3, GPIO.HIGH)
        time.sleep(INTERVAL/2.0)
        GPIO.output(3, GPIO.LOW)
        time.sleep(INTERVAL/2.0)

    # change direction
    GPIO.output(5, GPIO.LOW)

    for i in range(ACTUAL_STEPS):
        GPIO.output(3, GPIO.HIGH)
        time.sleep(INTERVAL/2.0)
        GPIO.output(3, GPIO.LOW)
        time.sleep(INTERVAL/2.0)
"""

