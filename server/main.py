#!/usr/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/test')
def test():
    test = "Test"
    return jsonify(test)

if __name__ == "__main__":
    app.run(debug=True)
