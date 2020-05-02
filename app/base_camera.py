import abc
import time
import threading
from greenlet import getcurrent as get_ident


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, app):
        """Start the background camera thread if it isn't running yet."""
        self.app = app
        app.logger.info("Initializing base camera class")

        self.thread = None  # background thread that reads frames from camera
        self.do_run = True  # Signal to keep recording
        self.frame = None  # current frame is stored here by background thread
        self.last_access = 0  # time of last client access to the camera
        self.event = CameraEvent()

    def start_recording(self):
        """Initialize background thread for capturing images from the camera implementation."""
        if self.thread is None:
            self.last_access = time.time()

            # start background frame thread
            self.thread = threading.Thread(target=self._thread)
            self.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def stop_recording(self):
        """Stop background thread and close camera."""
        self.do_run = False
        self.close_camera()
        # wait for camera cooldown
        time.sleep(1)

    @abc.abstractmethod
    def close_camera(self):
        """Close the camera."""

    @abc.abstractmethod
    def set_brightness(self):
        """Update the brightness value for the camera."""

    @abc.abstractmethod
    def set_vflip(self, value):
        """Toggle the vertical flip of the camera image."""

    @abc.abstractmethod
    def crop(self, crop_left, crop_right):
        """Crop the camera image."""

    @abc.abstractmethod
    def frames(self):
        """"Generator that returns frames from the camera."""

    def get_frame(self):
        """Return the current camera frame."""
        self.last_access = time.time()

        # wait for a signal from the camera thread
        self.event.wait()
        self.event.clear()

        return self.frame

    def _thread(self):
        """Camera background thread."""
        self.app.logger.info('Starting camera thread.')
        frames_iterator = self.frames()
        for frame in frames_iterator:
            self.frame = frame
            self.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - self.last_access > 10:
                frames_iterator.close()
                self.app.logger.info('Stopping camera thread due to inactivity.')
                break

            # End loop when do_run flag is set to False
            if not self.do_run:
                break

        self.thread = None
