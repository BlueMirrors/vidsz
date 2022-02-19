"""Defines interface for video reader
"""
import abc
from typing import Union, List

import numpy as np


class IReader(metaclass=abc.ABCMeta):
    """Video Reader Interface which will be implemented
    for every supported backend.
    """
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of Video Source

        Returns:
            str: name of video source
        """
        ...

    @property
    @abc.abstractmethod
    def width(self) -> int:
        """Width of Video

        Returns:
            int: width of video frame
        """
        ...

    @property
    @abc.abstractmethod
    def height(self) -> int:
        """Height of Video

        Returns:
            int: height of video frame
        """
        ...

    @property
    @abc.abstractmethod
    def fps(self) -> float:
        """FPS of Video

        Returns:
            float: fps of video
        """
        ...

    @property
    @abc.abstractmethod
    def backend(self) -> str:
        """Name of the Backend being used

        Returns:
            str: current backend name
        """
        ...

    @property
    @abc.abstractmethod
    def info(self) -> dict:
        """Video information

        Returns:
            dict: info of width, height, fps and backend.
        """
        ...

    @property
    @abc.abstractmethod
    def frame_count(self) -> int:
        """Total frames read

        Returns:
            int: read frames' count
        """
        ...

    @property
    @abc.abstractmethod
    def seconds(self) -> float:
        """Total seconds read

        Returns:
            float: read frames' in seconds
        """
        ...

    @property
    @abc.abstractmethod
    def minutes(self) -> float:
        """Total minutes read

        Returns:
            float: read frames' in minutes
        """
        ...

    @abc.abstractmethod
    def is_open(self) -> bool:
        """Checks if video is still open and last read frame was valid

        Returns:
            bool: True if video is open and last frame was not None, false otherwise.
        """
        ...

    @abc.abstractmethod
    def read(self) -> Union[np.ndarray, None]:
        """Returns next frame from the video if available

        Returns:
            Union[np.ndarry, None]: next frame if available, None otherwise.
        """
        ...

    @abc.abstractmethod
    def release(self) -> None:
        """Release Resources
        """
        ...

    @abc.abstractmethod
    def __del__(self) -> None:
        """Release Resources
        """
        ...

    @abc.abstractmethod
    def __next__(self) -> np.ndarray:
        """Returns next frame from the video

        Raises:
            StopIteration: No more frames to read

        Returns:
            np.ndarray: frame read from video
        """
        ...

    @abc.abstractmethod
    def __iter__(self) -> "IReader":
        """Returns iterable object for reading frames

        Returns:
            Iterable[IReader]: iterable object for reading frames
        """
        ...

    @abc.abstractmethod
    def __repr__(self) -> str:
        """Video's Info

        Returns:
            str: info
        """
        ...

    @abc.abstractmethod
    def __str__(self) -> str:
        """Video's Info

        Returns:
            str: Info
        """
        ...

    @abc.abstractmethod
    def __enter__(self) -> "IReader":
        """Returns Conext for "with" block usage

        Returns:
            IReader: Video Reader object
        """
        ...

    @abc.abstractmethod
    def __exit__(self, exc_type: None, exc_value: None,
                 traceback: None) -> None:
        """Release resources before exiting the "with" block

        Args:
            exc_type (NoneType): Exception type if any
            exc_value (NoneType): Exception value if any
            traceback (NoneType): Traceback of Exception
        """
        ...
