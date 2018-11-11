#!/usr/bin/env python
from flask import Flask, render_template, Response
from flask import request
import pigpio #Handling I/O ports
from PIcamera import Camera #Camera class which handles camera events and so on
from flask_socketio import SocketIO, emit
from Car import Car
from threading import Lock
import time

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet", engineio_logger=False)
carRPi = Car() #car instance for controling motors and servo
thread_lock = Lock()


@app.route('/ajax')
def index():
    """Home page for AJAX controll request"""
    if not cam.activeClient:
        return render_template('accelRotated.html')
    return Response("There is active client")


@app.route("/ws")
def indexWS():
    """Home page for controll over webSockets"""
    if not cam.activeClient:
        return render_template('accelRotatedWS.html')
    return Response("There is active client")


@app.route('/poweroff',  methods=['GET', 'POST'])
def powerOff():
    """shutdown the Pi"""
    try:
        if request.method == "POST":
            state = request.json["state"]
            if state == "off":
                from subprocess import call
                time.sleep(2)
                #first stop the car
                carRPi.stop()
                #and center the wheels
                carRPi.turn(70)
                #now shutdown
                call("sudo shutdown -h now", shell=True)

            return Response("Good")
        else:
            return Response("Bad request")

    except Exception as err:
        print(err)
        return Response("ERR")


@app.route('/getnumber',  methods=['GET', 'POST'])
def getNumber():
    """Handles AJAX requests with data saying what we should give to the servo --- handles turn"""
    try:
        if request.method == "POST":
            num = float(request.json["val"])
            print(num)
            carRPi.turn(num)

            return Response("Good")
        else:
            return Response("Bad request")

    except Exception as err:
        print(err)
        return Response("ERR")


@app.route('/getpower',  methods=['GET', 'POST'])
def getPower():
    """Handles AJAX requests with data saying what we should give to the H-bridge --- handles motor speed and direction"""
    try:
        if request.method == "POST":
            pow = float(request.json["pow"])
            print(pow)
            carRPi.setSpeed(pow)

            return Response("Good")
        else:
            return Response("Bad request")

    except Exception as err:
        print(err)
        return Response("ERR")


@app.route('/stream')
def video_stream():
    """Handles PICamera stream uses the generator func"""
    global cam
    if not cam.activeClient:
        with thread_lock:
            cam.activeClient = True
            print("Sending frames")
        #sends the header information about response type and generator then continues is sending frames
        return Response(streamGen(cam),
                        mimetype='multipart/x-mixed-replace; boundary=jpg')

    return Response("There is active client")


@socketio.on('turn', namespace="/controll")
def makeTurn(data):
    val = data["val"]
    #print("val:", val)
    carRPi.turn(val)


@socketio.on("speed", namespace="/controll")
def setSpeed(data):
    pow = data["pow"]
    #print("pow:", pow)
    carRPi.setSpeed(pow)


def streamGen(camera):
    """Video streaming generator  function."""
    while True:
        img = camera.get_img()
        yield (b'--jpg\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')


if __name__ == '__main__':
    app.debug = True

    #create camera instance
    cam = Camera(carRPi)
    cam.activeClient = False
    #run server on default port - 5000
    socketio.run(app, debug=True, host='0.0.0.0', use_reloader=False)
