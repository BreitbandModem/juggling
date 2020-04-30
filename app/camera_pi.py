import io
import time
import picamera
from base_camera import BaseCamera


class RaspiCamera(BaseCamera):

    def __init__(self, app):
        """Simple Picamera implementation."""
        super().__init__(app)
        self.app.logger.info("Initializing picamera camera.")

        self.start_recording()

    def set_brightness(self, brightness):
        self.app.logger.warning("Picamera Camera does not support brightness.")

    def frames(self):
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
