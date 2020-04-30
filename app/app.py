#!/usr/bin/env python
import logging
from flask import Flask, render_template, Response, request

# Import different camera sources
from camera_pi import RaspiCamera
from camera_mock import MockCamera
from image_processing import CvCamera

app = Flask(__name__)
camera = None


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    # Catch ajax request with form data
    if request.method == 'POST':

        brightness = request.form.get('brightness')
        if brightness is not None:
            app.logger.info('Form brightness submitted: %s', brightness)
            camera.set_brightness(brightness)

        input_selection = request.form.get('inputSelection')
        if input_selection is not None:
            app.logger.info('Form input selection: %s', input_selection)

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
    camera = MockCamera(app)

    # Init Flask (setting debug=True leads to camera failure on raspberry pi: out of resources)
    app.run(host='0.0.0.0', threaded=True, debug=False)
