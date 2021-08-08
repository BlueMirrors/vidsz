"""Defines interface for video writer
"""
import abc
from typing import List, Union

import numpy as np

from .reader import IReader


class IWriter(metaclass=abc.ABCMeta):
    """Video Writing Interface which will be implemented
    for every supported backend.
    """
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of Output Video

        Returns:
            str: name of output video
        """
        ...

    @property
    @abc.abstractmethod
    def width(self) -> int:
        """Width of Output Video

        Returns:
            int: width of video frame
        """
        ...

    @property
    @abc.abstractmethod
    def height(self) -> int:
        """Height of Output Video

        Returns:
            int: height of video frame
        """
        ...

    @property
    @abc.abstractmethod
    def fps(self) -> float:
        """FPS of Output Video

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
    def ext(self) -> str:
        """Extension of Output Video

        Returns:
            str: ext of video
        """
        ...

    @property
    @abc.abstractmethod
    def info(self) -> dict:
        """Video information

        Returns:
            dict: info of width, height, fps, backend and ext
        """
        ...

    @property
    @abc.abstractmethod
    def frame_count(self) -> int:
        """Total frames written

        Returns:
            int: written frames' count
        """
        ...

    @property
    @abc.abstractmethod
    def seconds(self) -> float:
        """Total seconds written

        Returns:
            float: written frames' in seconds
        """
        ...

    @property
    @abc.abstractmethod
    def minutes(self) -> float:
        """Total minutes written

        Returns:
            float: written frames' in minutes
        """
        ...

    @abc.abstractmethod
    def is_open(self) -> bool:
        """Checks if writer is still open

        Returns:
            bool: True if writer is open, False otherwise
        """
        ...

    @abc.abstractmethod
    def write(self, frame: np.ndarray) -> None:
        """Write frame to output video

        Args:
            frame (np.ndarray): frame to write
        """
        ...

    @abc.abstractmethod
    def write_all(self, frames: Union[List[np.ndarray], IReader]) -> None:
        """Write all frames to output video

        Args:
            frames (Union[List[np.ndarray], IReader]): Iterable object that contains frames.
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
    def __repr__(self) -> str:
        """Writer's Info
        Returns:
            str: info
        """
        ...

    @abc.abstractmethod
    def __str__(self) -> str:
        """Writer's Info
        Returns:
            str: info
        """
        ...

    @abc.abstractmethod
    def __enter__(self) -> "IWriter":
        """Returns Conext for "with" block usage
        Returns:
            IWriter: Video Reader object
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
