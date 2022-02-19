"""Implements vidsz.interfaces.IReader interface for OpenCV Backend.
"""
from typing import Optional, Union, List

import cv2
import numpy as np

from vidsz.interfaces import IReader


class Reader(IReader):
    """Video Reading wrapper around Opencv-Backend
    """
    def __init__(self,
                 source_name: Union[str, int],
                 batch_size: Optional[int] = None,
                 dynamic_batch: Optional[bool] = False,
                 **kwargs) -> None:
        """Initiate Reader object

        Args:
            source_name (Union[str, int]): Name/URL/Path to video source

            batch_size (Optional[int]): number of frames to return (as one batch) for one read.
            Defaults to None will return images individually without batch axis.

            dynamic_batch (Optional[bool]): if set to True then last batch of frames may have
            less than batch_size frames (depending on how many frames were left for last batch).
            If set to False, last batch may have some frames made up of zeros to match batch_size.
            Defaults to False.
        """
        # initiate props
        self._initiate_props()

        # sanity conversion
        self._name = str(source_name)

        # set batch
        self._batch_size = batch_size
        self._dynamic_batch = dynamic_batch

        # open video stream
        self._video_stream = cv2.VideoCapture(
            int(self._name) if self._name.isdigit() else self._name)

        # update info with current video stream
        self._update_info()

    def _initiate_props(self) -> None:
        """Initiate all class properties to default values
        """
        self._name = None
        self._is_open = True
        self._video_stream = None
        self._width = None
        self._height = None
        self._fps = None
        self._backend = 'opencv'
        self._info = None
        self._frame_count = 0
        self._seconds = 0
        self._minutes = 0
        self._batch_size = None
        self._dynamic_batch = False

    def _update_info(self) -> None:
        """Update info property according to currently open video stream

        Raises:
            Exception: VideoSourceNotOpen raised when no video stream is opened
        """
        # check if source is open
        if not self.is_open():
            raise Exception((f"Failed to read from {self.name}. " +
                             "Please check the filename/source-info again."))

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
        """Video information

        Returns:
            dict: info of width, height, fps and backend.
        """
        return self._info

    @property
    def frame_count(self) -> int:
        """Total frames read

        Returns:
            int: read frames' count
        """
        return self._frame_count

    @property
    def seconds(self) -> float:
        """Total seconds read

        Returns:
            float: read frames' in seconds
        """
        return (self._frame_count / self._fps) if self._fps else 0

    @property
    def minutes(self) -> float:
        """Total minutes read

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

    def read_frame(self) -> Union[np.ndarray, None]:
        """Returns next frame from the video if available

        Returns:
            Union[np.ndarry, None]: next frame if available, None otherwise.
        """
        flag, frame = self._video_stream.read()
        self._frame_count += 0 if frame is None else 1
        self._is_open = flag
        return frame

    def read_batch(self) -> Union[np.ndarray, None]:
        """Returns next batch of frames from the video if available

        Returns:
            Union[np.ndarry, None]: next batch if available, None otherwise.
        """
        if not self.is_open():
            return None

        # pre-allocate batch
        batch = np.zeros((self._batch_size, self.height, self.width, 3), dtype="uint8")

        # fill batch
        for i in range(self._batch_size):
            # read frame
            frame = self.read_frame()

            # stop process, no frames left
            if frame is None:
                # decrm index because this frame was empty
                i -= 1
                break

            # add to batch
            batch[i] = frame

        return batch[:i + 1] if self._dynamic_batch else batch

    def read(self) -> Union[np.ndarray, None]:
        """Returns next frame or batch of frames from the video if available

        Returns:
            Union[np.ndarry, None]: next frame or batch of frames if available, None otherwise.
        """
        if self._batch_size is None:
            return self.read_frame()
        return self.read_batch()

    def release(self) -> None:
        """Release Resources
        """
        if self._video_stream is not None:
            self._video_stream.release()

    def __del__(self) -> None:
        """Release Resources
        """
        self.release()
        self._video_stream = None

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
        """Returns Conext for "with" block usage

        Returns:
            Reader: Video Reader object
        """
        return self

    def __exit__(self, exc_type: None, exc_value: None,
                 traceback: None) -> None:
        """Release resources before exiting the "with" block

        Args:
            exc_type (NoneType): Exception type if any
            exc_value (NoneType): Exception value if any
            traceback (NoneType): Traceback of Exception
        """
        self.release()
