import io
import time
import picamera
from base_camera import BaseCamera


class RaspiCamera(BaseCamera):

    def __init__(self, app):
        """Simple Picamera implementation."""
        super().__init__(app)
        self.app.logger.info("Initializing picamera camera.")

        self.camera = picamera.PiCamera()

        self.start_recording()

    def close_camera(self):
        self.camera.close()

    def set_vflip(self, value):
        self.camera.vflip = value

    def crop(self, crop_left, crop_right):
        pass

    def set_brightness(self, brightness):
        self.app.logger.warning("Picamera Camera does not support brightness.")

    def frames(self):
        # let camera warm up
        time.sleep(1)

        stream = io.BytesIO()
        for _ in self.camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
            # return current frame
            stream.seek(0)
            yield stream.read()

            # reset stream for next frame
            stream.seek(0)
            stream.truncate()
