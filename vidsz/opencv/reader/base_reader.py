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

        # update info
        self._info = {
            "name": self._name,
            "width": self._width,
            "height": self._height,
            "fps": self._fps,
            "backend": self._backend
        }
