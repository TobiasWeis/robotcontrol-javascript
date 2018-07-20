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

ql = Queue()
qs = Queue()
qs2 = Queue()
qb = Queue()
qb2 = Queue()

try:
    from Linear import *
    linear = Linear(ql)
    linear.start()

    from Servo import *
    servo = Servo(qs, 7)
    servo.start()
    servo2 = Servo(qs2, 11)
    servo2.start()

    from Binary import *
    binary = Binary(qb, 13, axis="A")
    binary.start()

    binary2 = Binary(qb2,15, axis="B")
    binary2.start()

except Exception, e:
    print("Could not import robot")
    print e


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
        x = data["left"][0]
        y = data["left"][1]
        ql.put(("left",x,y))
        print "Left: ",x,",",y
    elif "right" in data.keys():
        x = data["right"][0]
        y = data["right"][1]
        qs.put(("right",x,y))
        qs2.put(("right",y,x))
        print "Right: ",x,",",y
    elif "A" in data.keys():
        qb.put(("A",1,0))
        print "A"
    elif "B" in data.keys():
        qb2.put(("B",1,0))
        print "B"

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
