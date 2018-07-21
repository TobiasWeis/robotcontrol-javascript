# robotcontrol-javascript
interactive control interface for robots and other electronics experiments

this software provides
* an interactive GUI served as a webpage
* a server that runs on a robot (raspberry pi)
* a two-way websocket connection for low latency control
* some server-side robot-classes (servo-, stepper-, toggle-control) that are already mapped to control inputs

## requirements
* python, numpy, flask

## howto run
* run flask-server (server/main.py) -> this will provide the websocket API and serve the webpage on port 5000 
* call interface webpage in browser: http://server-ip:5000

## TODO
* unify control-interface to allow easier mapping of interface-axis/buttons to robot actions
