import time
from base_camera import BaseCamera


class MockCamera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    imgs = [open('/usr/src/app/res/' + file, 'rb').read() for file in ['1.jpg', '2.jpg', '3.jpg']]

    @staticmethod
    def frames():
        while True:
            time.sleep(1)
            yield MockCamera.imgs[int(time.time()) % 3]