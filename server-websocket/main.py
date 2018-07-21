#!/usr/bin/python
"""
We are using a small REST server to control our robot.
"""
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import math
from multiprocessing import Process, Queue

ql = Queue()
qs = Queue()
qs2 = Queue()
qb = Queue()
qb2 = Queue()

try:
    from robot.Linear import *
    linear = Linear(ql)
    linear.start()

    from robot.Servo import *
    servo = Servo(qs, 7)
    servo.start()
    servo2 = Servo(qs2, 11)
    servo2.start()

    from robot.Binary import *
    binary = Binary(qb, 13, axis="A")
    binary.start()

    binary2 = Binary(qb2,15, axis="B")
    binary2.start()
except Exception, e:
    print("Could not import robot")
    print e


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
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
    return render_template('index.html')


@socketio.on('request', namespace='/status')
def send_status():
    print "send_status"
    emit('status', {'data':"Here could be your status"})

@socketio.on('connect', namespace='/status')
def connect_status():
    print "Status connected"

@socketio.on('connect', namespace='/control')
def connect_status():
    print "Control connected"

@socketio.on_error_default
def default_error_handler(e):
    print "======================= ERROR"
    print(request.event["message"]) # "my error event"
    print(request.event["args"])    # (data,)"

@socketio.on('control', namespace='/control')
def control(message):
    print "control"
    data = message["data"]
    print data
    if "left" in data.keys():
        x = data["left"][0]
        y = data["left"][1]
        print "Left: ",x,",",y
        ql.put(("left",x,y))
    elif "right" in data.keys():
        x = data["right"][0]
        y = data["right"][1]
        print "Right: ",x,",",y
        qs.put(("right",x,y))
        qs2.put(("right",y,x))
    elif "A" in data.keys():
        print "A"
        qb.put(("A",1,0))
    elif "B" in data.keys():
        print "B"
        qb2.put(("B",1,0))

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0')
    socketio.run(app, host="0.0.0.0", debug=True)
