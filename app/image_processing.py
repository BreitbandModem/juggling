import cv2
from base_camera import BaseCamera


class CvCamera(BaseCamera):
    camera = None

    def __init__(self, camera):
        CvCamera.camera = camera

    @staticmethod
    def frames():
        frames_iterator = CvCamera.camera.frames()
        for frame in frames_iterator:
            cv2_image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # Do image processing
            cv2.rotate(frame, cv2.ROTATE_180)

            image = cv2.imencode('.jpeg', cv2_image)
            yield image