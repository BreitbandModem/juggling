import cv2
import io
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from base_camera import BaseCamera


class CvCamera(BaseCamera):
    @staticmethod
    def frames():
        with PiCamera() as camera:
            # initialize the camera and grab a reference to the raw camera capture
            camera.resolution = (640, 480)
            camera.framerate = 32
            rawCapture = PiRGBArray(camera, size=(640, 480))

            # let camera warm up
            time.sleep(1)

            # capture frames from the camera
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # grab the raw NumPy array representing the image
                raw_image = frame.array

                # Do image processing
                cv2_image = cv2.rotate(raw_image, cv2.ROTATE_180)

                _, processed_image = cv2.imencode('.jpeg', cv2_image)
                yield processed_image.tostring()

                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
