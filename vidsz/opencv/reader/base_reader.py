"""Implements vidsz.interfaces._IReader interface for OpenCV Backend.
"""
from typing import Union, List

import cv2
import numpy as np

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
        self._width = int(self._video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._fps = self._video_stream.get(cv2.CAP_PROP_FPS)
        self._is_open = bool(self._video_stream.isOpened())

        # update info
        self._info = {
            "name": self._name,
            "width": self._width,
            "height": self._height,
            "fps": self._fps,
            "backend": self._backend
        }

    @property
    def name(self) -> str:
        """Name of Video Source

        Returns:
            str: name of video source
        """
        return self._name

    @property
    def width(self) -> int:
        """Width of Video

        Returns:
            int: width of video frame
        """
        return self._width

    @property
    def height(self) -> int:
        """Height of Video

        Returns:
            int: height of video frame
        """
        return self._height

    @property
    def fps(self) -> float:
        """FPS of Video

        Returns:
            float: fps of video
        """
        return self._fps

    @property
    def backend(self) -> str:
        """Name of the Backend being used

        Returns:
            str: current backend name
        """
        return self._backend

    @property
    def info(self) -> dict:
        """Video Informations

        Returns:
            dict: info of width, height, fps and backend.
        """
        return self._info

    @property
    def frame_count(self) -> int:
        """Number of frames already been read

        Returns:
            int: read frames' count
        """
        return self._frame_count

    @property
    def seconds(self) -> float:
        """Amount of seconds already been read

        Returns:
            float: read frames' in seconds
        """
        return (self._frame_count / self._fps) if self._fps else 0

    @property
    def minutes(self) -> float:
        """Amount of minutes already been read

        Returns:
            float: read frames' in minutes
        """
        return self.seconds / 60.0

    def is_open(self) -> bool:
        """Checks if video is still open and last read frame was valid

        Returns:
            bool: True if video is open and last frame was not None, false otherwise.
        """
        return self._video_stream.isOpened() and self._is_open

    def read(self) -> Union[np.ndarray, None]:
        """Returns next frame from the video if available

        Returns:
            Union[np.ndarry, None]: next frame if available, None otherwise.
        """
        flag, frame = self._video_stream.read()
        self._frame_count += 0 if frame is None else 1
        self._is_open = flag
        return frame

    def read_all(self) -> List[np.ndarray]:
        """Read all the frames into a list

        Returns:
            List[np.ndarray]: List containing all the remaining frames in Video
        """
        return [frame for frame in self]

    def release(self) -> None:
        """Release Resources
        """
        if self._video_stream is not None:
            self._video_stream.release()
            self._video_stream = None

    def __del__(self) -> None:
        """Release Resources
        """
        self.release()

    def __next__(self) -> np.ndarray:
        """Returns next frame from the video

        Raises:
            StopIteration: No more frames to read

        Returns:
            np.ndarray: frame read from video
        """
        frame = self.read()
        if frame is None:
            raise StopIteration()
        return frame

    def __iter__(self) -> "Reader":
        """Returns iterable object for reading frames

        Returns:
            Iterable[Reader]: iterable object for reading frames
        """
        return self

    def __repr__(self) -> str:
        """Video's Info

        Returns:
            str: info
        """
        return str(self._info)

    def __str__(self) -> str:
        """Video's Info

        Returns:
            str: Info
        """
        return str(self._info)

    def __enter__(self) -> "Reader":
        """Conext for with statement

        Returns:
            Reader: Video Reader object
        """
        return self

    def __exit__(self, exc_type: None, exc_value: None,
                 traceback: None) -> None:
        """Release resources before exit

        Args:
            exc_type (NoneType): Exception type if any
            exc_value (NoneType): Exception value if any
            traceback (NoneType): Traceback of Exception
        """
        self.release()
