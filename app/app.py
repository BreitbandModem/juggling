#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response


# Raspberry Pi camera module (requires picamera package)
from camera_pi import PiCamera

# Opencv camera module
from image_processing import CvCamera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(PiCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/processing_feed')
def processing_feed():
    """Video processing streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(CvCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
