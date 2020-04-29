from abc import ABC, abstractmethod
import cv2
import imutils
import math
from collections import deque
from collections import namedtuple
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from base_camera import BaseCamera


Position = namedtuple('Position', ['x', 'y', 'radius'])


class Ball:
    """A class representing a ball in an image

    CONSTANT Attributes
        COLOR_LOWER  The lower bound of the color range of a ball
        COLOR_UPPER  The upper bound of the color range of a ball
        MAX_DIST  The max distance to consider for connecting ball positions
        MAX_HISTORY The max number of positions to remember
        MAX_NUM_BALLS  The maximum number of balls to keep track of

    Class Attributes
        balls  The list (deque) of tracked balls
    """

    COLOR_LOWER = (0, 0, 190)
    COLOR_UPPER = (179, 65, 255)
    DRAW_COLOR = (0, 255, 255)
    DRAW_THICKNESS = 2

    MAX_DIST = 100
    MAX_HISTORY = 200
    MAX_NUM_BALLS = 3

    balls = deque(maxlen=MAX_NUM_BALLS)

    def __init__(self, pos):
        self.positions = deque(maxlen=Ball.MAX_HISTORY)
        self.positions.appendleft(pos)

    def update_position(self, pos):
        self.positions.appendleft(pos)

    def draw_ball(self, frame, index):
        cv2.circle(
            frame,
            (self.positions[index].x, self.positions[index].y),
            self.positions[index].radius,
            Ball.DRAW_COLOR,
            Ball.DRAW_THICKNESS
        )

    @staticmethod
    def calc_distance(ball1, ball2):
        """ Returns the distance between two balls latest position """
        x_diff = ball1.positions[0].x - ball2.positions[0].x
        y_diff = ball1.positions[0].y - ball2.positions[0].y
        distance = math.sqrt((x_diff ** 2) + (y_diff ** 2))
        return distance

    @classmethod
    def draw_path(cls, frame):
        """ Connects all previous positions of each ball with lines """
        for ball in cls.balls:
            ball.draw_ball(frame, 0)

            for i in range(0, len(ball.positions) - 1):
                cv2.line(
                    frame,
                    (ball.positions[i].x, ball.positions[i].y),
                    (ball.positions[i + 1].x, ball.positions[i + 1].y),
                    cls.DRAW_COLOR,
                    cls.DRAW_THICKNESS
                )

    @classmethod
    def draw_latest(cls, frame):
        """ Draws circles around the latest positions of all balls """
        for ball in cls.balls:
            ball.draw_ball(frame, 0)

    @classmethod
    def apply_location(cls, x, y, radius):
        """ Allocates a new position to an existing ball or creates a new ball """
        new_ball = cls(Position(x, y, radius))

        max_dist = cls.MAX_DIST
        nearest_ball = None
        for ball in cls.balls:
            distance = cls.calc_distance(new_ball, ball)
            if distance < max_dist:
                max_dist = distance
                nearest_ball = ball

        if nearest_ball is not None:
            nearest_ball.update_position(new_ball.positions[0])
        else:
            cls.balls.append(new_ball)


class Processor(ABC):
    """ Abstract Static Class for processing cv2 frames """

    @classmethod
    @abstractmethod
    def process_frame(cls, frame):
        pass


class Detector(Processor):
    """ Static Class that detects ball shapes """

    @staticmethod
    def prepare_frame(frame):
        """ resize the frame, blur it, and convert it to the HSV color space """
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        return frame, hsv

    @staticmethod
    def apply_mask(hsv):
        """ construct a mask for the ball color, then perform
        a series of dilations and erosions to remove any small
        blobs left in the mask
        """
        mask = cv2.inRange(hsv, Ball.COLOR_LOWER, Ball.COLOR_UPPER)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        return mask

    @staticmethod
    def find_large_contours(mask, minratio):
        """ Returns all sufficiently large contours """
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if len(cnts) == 0:
            return cnts

        # Find the largest contour in the mask, then use
        # it to compute the minimum radius (50% smaller)
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        min_radius = minratio * radius

        # loop over all contours which are large enough
        large_cnts = []
        for cnt in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            if radius > min_radius:
                large_cnts.append(cnt)

        return large_cnts

    @classmethod
    def process_frame(cls, frame):
        """ Filters the frame for ball like contours and creates Ball objects thereof """
        frame, hsv = cls.prepare_frame(frame)

        mask = cls.apply_mask(hsv)

        cnts = cls.find_large_contours(mask, 0.5)

        for cnt in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            Ball.apply_location(int(x), int(y), int(radius))

        Ball.draw_path(frame)

        return frame


class CvCamera(BaseCamera):
    @staticmethod
    def frames():
        with PiCamera() as camera:
            # initialize the camera and grab a reference to the raw camera capture
            # camera.resolution = (640, 480)
            camera.resolution = (1280, 720)
            camera.framerate = 90
            camera.rotation = 180
            camera.brightness = 75  # integer between 0 and 100
            camera.contrast = 30  # integer between -100 and 100

            rawCapture = PiRGBArray(camera, size=(1280, 720))

            # let camera warm up
            time.sleep(1)

            # capture frames from the camera
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # grab the raw NumPy array representing the image
                raw_image = frame.array

                # Do image processing
                frame = Detector.process_frame(frame)

                _, processed_image = cv2.imencode('.jpeg', raw_image)
                yield processed_image.tostring()

                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
