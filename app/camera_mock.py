import time
from base_camera import BaseCamera


class MockCamera(BaseCamera):

    def __init__(self, app):
        """An emulated camera implementation that streams a repeated sequence of
        files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
        super().__init__(app)
        self.app.logger.info("Initializing mock camera.")

        self.images = [open('/usr/src/app/res/' + file, 'rb').read() for file in ['1.jpg', '2.jpg', '3.jpg']]

        self.start_recording()

    def close_camera(self):
        pass

    def set_brightness(self, brightness):
        self.app.logger.warning("Mock Camera does not support brightness.")

    def frames(self):
        while True:
            time.sleep(1)
            yield self.images[int(time.time()) % 3]