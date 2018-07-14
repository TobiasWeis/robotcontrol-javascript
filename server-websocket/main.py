#!/usr/bin/python
"""
We are using a small REST server to control our robot.
"""
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import math
import json
from multiprocessing import Process, Queue

q = Queue()
try:
    from Linear import *
    linear = Linear(q)
    linear.start()
except:
    print("Could not import robot")


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)



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

"""
@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data':'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
"""

@socketio.on('request', namespace='/status')
def send_status():
    emit('status', {'data':"Here could be your status"})


@socketio.on('control', namespace='/control')
def control(message):
    data = message["data"]
    if "left" in data.keys():
        print "LEFT!"
        distance = data["left"][0]
        angle = data["left"][1]
        x,y = map_dist_angle(float(distance), float(angle))

        # put it in queue for Robot-class to receive
        q.put(x)
    elif "right" in data.keys():
        distance = data["right"][0]
        angle = data["right"][1]
    elif "A" in data.keys():
        print "Button A pressed"
    elif "B" in data.keys():
        print "Button B pressed"


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
    return jsonify(status)

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0')
    socketio.run(app, host="0.0.0.0")
