#!/usr/bin/python
"""
We are using a small REST server to control our robot
"""
from flask import Flask, jsonify
import math

app = Flask(__name__)

# FIXME: put this in another file later
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
    return "Hello World"

@app.route('/left/<distance>/<angle>')
def left(distance,angle):
    """
    inputs of the left virtual joystick
    - when the user lets go of it, it will send a 0,0
    """
    distance = float(distance)
    angle = float(angle)

    x,y = map_dist_angle(distance, angle)
    print "Inputs: DISTANCE: ",distance,",ANGLE: ",angle,", X:",x,", Y:",y
    ret = "OK"
    return jsonify(ret)

if __name__ == "__main__":
    app.run(debug=True)
