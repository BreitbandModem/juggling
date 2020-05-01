#!/usr/bin/env python
import logging
from enum import IntEnum
from flask import Flask, render_template, Response, request

# Import different camera sources
from camera_pi import RaspiCamera
from camera_mock import MockCamera
from image_processing import CvCamera


class Input(IntEnum):
    MOCK = 0
    PICAM = 1
    CV2PICAM = 2


app = Flask(__name__)
camera = None
selected_input = {Input.MOCK: 'selected=selected',
                  Input.PICAM: '',
                  Input.CV2PICAM: ''}


@app.route('/', methods=['GET'])
def index():
    """Video streaming home page."""
    return render_template('index.html', selected_input=selected_input)


@app.route('/brightness', methods=['POST'])
def brightness():
    """Set brightness value for camera."""
    # Catch ajax request with form data
    brightness_val = 'error'
    if request.method == 'POST':
        brightness_val = request.form.get('brightness')
        if brightness_val is not None:
            app.logger.info('Form brightness submitted: %s', brightness_val)
            camera.set_brightness(brightness_val)

    return {'brightness': brightness_val}


@app.route('/vflip', methods=['POST'])
def vflip():
    """Toggle vertical flipping of camera image."""
    # Catch ajax request with form data
    vflip_val = 'error'
    if request.method == 'POST':
        vflip_val = request.form.get('vflip')
        app.logger.info('vflip: '+vflip_val)
        if vflip_val is not None:
            app.logger.info('Form brightness submitted: %s', vflip_val)
            camera.set_vflip(vflip_val == 'true')

    return {'brightness': vflip_val}


@app.route('/input-selection', methods=['POST'])
def input_selection():
    """Select Camera image to display."""
    # Catch ajax request with form data
    input_select = request.form.get('inputSelection')
    app.logger.info('Form input selection: %s', input_select)

    try:
        input = int(input_select)
        app.logger.info('my int: %d', input)

        global camera
        camera.stop_recording()
        camera = {
            Input.MOCK: lambda: MockCamera(app),
            Input.PICAM: lambda: RaspiCamera(app),
            Input.CV2PICAM: lambda: CvCamera(app)
        }[input]()

    except ValueError:
        input_select = 'error'

    return {'inputSelection': input_select}


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
    camera = MockCamera(app)

    # Init Flask (setting debug=True leads to camera failure on raspberry pi: out of resources)
    app.run(host='0.0.0.0', threaded=True, debug=False)
