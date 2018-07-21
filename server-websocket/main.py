#!/usr/bin/python
"""
We are using a small REST server to control our robot.
"""
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import math
from multiprocessing import Process, Queue

_debug = False


# TODO: axis-mapping should be OOP and automatic!

try:
    from robot.Linear import *
    linear = Linear(Queue(), verbose=False)
    linear.start()

    from robot.Servo import *
    servo = Servo(Queue(), 7, verbose=False)
    servo.start()
    servo2 = Servo(Queue(), 11, verbose=False)
    servo2.start()

    from robot.Binary import *
    binary = Binary(Queue(), 13, axis="A", verbose=False)
    binary.start()

    binary2 = Binary(Queue(),15, axis="B", verbose=False)
    binary2.start()
except Exception, e:
    print("Could not import robot")
    print e


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on_error_default
def default_error_handler(e):
    print "======================= ERROR"
    print(request.event["message"])
    print(request.event["args"])


@socketio.on('control', namespace='/control')
def control(message):
    data = message["data"]
    if "left" in data.keys():
        x = data["left"][0]
        y = data["left"][1]
        if _debug: print "[Server] Left: ",x,",",y
        linear.q.put(("left",x,y))
    elif "right" in data.keys():
        x = data["right"][0]
        y = data["right"][1]
        if _debug: print "[Server] Right: ",x,",",y
        servo.q.put(("right",x,y))
        servo2.q.put(("right",y,x))
    elif "A" in data.keys():
        if _debug: print "[Server] A"
        binary.q.put(("A",1,0))
    elif "B" in data.keys():
        if _debug: print "[Server] B"
        binary2.q.put(("B",1,0))

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True, use_reloader=False)
