"""Implements vidsz.interfaces._IReader interface for OpenCV Backend.
"""
from typing import Union

import cv2

from vidsz.interfaces import _IReader


class Reader(_IReader):
    """Video Reading wrapper around Opencv-Backend
    """
    def __init__(self, source_name: Union[str, int], **kwargs) -> None:
        """Initiate Reader object

        Args:
            source_name (Union[str, int]): Name/URL/Path to video source
        """
        # initiate props
        self._initiate_props()

        # sanity conversion
        self._name = str(source_name)

        # open video stream
        self._video_stream = cv2.VideoCapture(
            int(self._name) if self._name.isdigit() else self._name)

        # update info with current video stream
        self._update_info()

    def _initiate_props(self) -> None:
        """Initiate all class properties to default values
        """
        self._name = None
        self._is_open = False
        self._video_stream = None
        self._width = None
        self._height = None
        self._fps = None
        self._backend = 'opencv'
        self._info = None
        self._frame_count = 0
        self._seconds = 0
        self._minutes = 0

    def _update_info(self) -> None:
        """Update info property according to currently open video stream

        Raises:
            Exception: VideoSourceNotOpen raised when no video stream is opened
        """
        if self._video_stream is None:
            raise Exception(
                "VideoSourceNotOpen: Cannot access video properties for non-opened source."
            )

        # update relevant props
        self._width = self._video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        self._height = self._video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self._fps = self._video_stream.get(cv2.CAP_PROP_FPS)
        self._is_open = self._video_stream.isOpened()

        # update info
        self._info = {
            "name": self._name,
            "width": self._width,
            "height": self._height,
            "fps": self._fps,
            "backend": self._backend
        }

    @property
    def name(self):
        return self._name

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def fps(self):
        return self._fps

    @property
    def backend(self):
        return self._backend

    @property
    def info(self):
        return self._info

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def seconds(self):
        return (self._frame_count / self._fps) if self._fps else 0

    @property
    def minutes(self):
        return self.seconds / 60.0

    def is_open(self):
        return self._video_stream.isOpened() and self._is_open

    def read(self):
        flag, frame = self._video_stream.read()
        self._frame_count += 0 if frame is None else 1
        self._is_open = flag
        return frame

    def read_all(self):
        return [frame for frame in self]

    def release(self):
        if self._video_stream is not None:
            self._video_stream.release()
            self._video_stream = None

    def __del__(self):
        self.release()

    def __next__(self):
        frame = self.read()
        if frame is None:
            raise StopIteration()
        return frame

    def __iter__(self):
        return self

    def __repr__(self):
        return str(self._info)

    def __str__(self):
        return str(self._info)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
