#!/usr/bin/python
"""
We are using a small REST server to control our robot.
"""
from flask import Flask, jsonify
import math
from multiprocessing import Process, Queue

try:
    from Linear import *
    linear = Linear(q)
    linear.start()
except:
    print "Could not import robot"


app = Flask(__name__)
q = Queue()


def map_dist_angle(distance, angle):
    """
    map distance and angle values to independent x/y axis values,
    angle is in degrees, distance is normalized to diameter of joystick circle
    """
    x = distance * math.cos(math.radians(angle))
    y = distance * math.sin(math.radians(angle))

    return x,y


@app.route('/')
def index():
    return "Robot-Control"

@app.route('/axis/<num>/<distance>/<angle>')
def left(num,distance,angle):
    """
    inputs of the virtual joysticks
    - when the user lets go of it, it will send a 0,0

    """
    x,y = map_dist_angle(float(distance), float(angle))

    # put it in queue for Robot-class to receive
    q.put(x)

    ret = "OK"
    return jsonify(ret)

@app.route('/status')
def status():
    status = {}
    status["Test1"] = "test1"
    status["Test2"] = "test2"
    return jsonify(test="Test")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
