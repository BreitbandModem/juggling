import cv2
import io
import time
import picamera
from base_camera import BaseCamera


class CvCamera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                               use_video_port=True):
                # return current frame
                stream.seek(0)
                cv2_image = cv2.imdecode(stream.read(), cv2.IMREAD_COLOR)

                # Do image processing
                cv2.rotate(cv2_image, cv2.ROTATE_180)

                image = cv2.imencode('.jpeg', cv2_image)
                yield image

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
