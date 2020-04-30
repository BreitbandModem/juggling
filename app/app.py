#!/usr/bin/env python
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, Response, request

# Import different camera sources
from camera_pi import PiCamera
from camera_mock import MockCamera
from image_processing import CvCamera

app = Flask(__name__)
camera = None


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    if request.method == 'POST':
        param = request.form
        app.logger.info('Form submitted: %s', param)
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
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # Init Logger
    logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(filename='/logs/app.log', level=logging.DEBUG)
    app.logger.info('Hello Logger')

    # Init default Camera (cv2+picamera)
    camera = MockCamera()

    # Init Flask
    app.run(host='0.0.0.0', threaded=True, debug=True)
