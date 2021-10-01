"""Implements vidsz.interfaces.IWriter interface for OpenCV Backend.
"""
import os
from typing import Optional, List, Union

import cv2
import numpy as np

from vidsz.interfaces import IWriter
from vidsz.interfaces import IReader


class Writer(IWriter):
    """Video Writing wrapper around Opencv-Backend
    """

    # opencv fourcc mappings
    _EXT_TO_FOURCC = {".avi": "DIVX", ".mkv": "X264", ".mp4": "mp4v"}

    def __init__(self,
                 reader: Optional[IReader] = None,
                 name: Optional[str] = None,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 fps: Optional[int] = None,
                 ext: Optional[str] = None) -> None:
        """Initiate Writer object

        Args:
            reader (Optional[IReader], optional): Source for setting
            output video's configs. Defaults to None.

            name (Optional[str], optional): name of output video,
            overwrites reader's. Defaults to None.

            width (Optional[int], optional): width of output video,
            overwrites reader's. Defaults to None.

            height (Optional[int], optional): height of output video.
            overwrites reader's. Defaults to None.

            fps (Optional[int], optional): fps of output video,
            overwrites reader's. Defaults to None.

            ext (Optional[str], optional): extension of output video,
            overwrites reader's. Defaults to None.
        """

        # initiate props
        self._initiate_props()

        # update props if provided
        self._update_props(reader, name, width, height, fps, ext)

        # initiate writer
        self._video_writer = cv2.VideoWriter(self._name, self._fourcc(),
                                             self._fps,
                                             (self._width, self._height))

        # check if open
        if not self.is_open():
            raise AssertionError(
                "Failed to Create Writer for the given settings.")

        # update info
        self._update_info()

    def _initiate_props(self) -> None:
        """Initiate all class properties to default values
        """
        self._name = None
        self._video_writer = None
        self._width = None
        self._height = None
        self._fps = None
        self._backend = "opencv"
        self._ext = None
        self._info = None
        self._frame_count = 0
        self._seconds = 0
        self._minutes = 0

    def _update_props(self,
                      reader: Optional[IReader] = None,
                      name: Optional[str] = None,
                      width: Optional[int] = None,
                      height: Optional[int] = None,
                      fps: Optional[int] = None,
                      ext: Optional[str] = None) -> None:
        """Update all relevant class properties

        Args:
            reader (Optional[IReader], optional): Source for setting
            output video's configs. Defaults to None.

            name (Optional[str], optional): name of output video,
            overwrites reader's. Defaults to None.

            width (Optional[int], optional): width of output video,
            overwrites reader's. Defaults to None.

            height (Optional[int], optional): height of output video.
            overwrites reader's. Defaults to None.

            fps (Optional[int], optional): fps of output video,
            overwrites reader's. Defaults to None.

            ext (Optional[str], optional): extension of output video,
            overwrites reader's. Defaults to None.

        Raises:
            Exception: Raised if neither reader nor name is given.
        """

        # set default if given
        if reader is not None:
            reader_name, reader_ext = os.path.splitext(reader.name)
            self._name = f"{reader_name}_out{reader_ext}"
            self._width = reader.width
            self._height = reader.height
            self._fps = reader.fps

        # override props if given
        if name is not None:
            self._name = name
        if width is not None:
            self._width = width
        if height is not None:
            self._height = height
        if fps is not None:
            self._fps = fps

        # check valid name
        if self._name is None:
            raise AssertionError("Must provide either Reader or name arg.")

        # set ext for CV2 writer creations
        self._ext = os.path.splitext(self._name)[1] if ext is None else ext

        # add . for consistency
        if '.' not in self._ext:
            self._ext = '.' + self._ext

    def _update_info(self) -> None:
        """Update info property according to class props
        """
        # update info
        self._info = {
            "name": self._name,
            "width": self._width,
            "height": self._height,
            "fps": self._fps,
            "backend": self._backend,
            "ext": self._ext
        }

    def _fourcc(self) -> cv2.VideoWriter_fourcc:
        """Returns CV2 VideoWriter_fourcc for writer's ext

        Raises:
            NotImplementedError: raise if unsupported ext is used.

        Returns:
            cv2.VideoWriter_fourcc: fourcc of used ext
        """
        if self._ext not in self._EXT_TO_FOURCC:
            raise NotImplementedError(f"'{self._ext}'is not supported.")
        return cv2.VideoWriter_fourcc(*self._EXT_TO_FOURCC[self._ext])

    @property
    def name(self) -> str:
        """Name of Output Video

        Returns:
            str: name of output video
        """
        return self._name

    @property
    def width(self) -> int:
        """Width of Output Video

        Returns:
            int: width of video frame
        """
        return self._width

    @property
    def height(self) -> int:
        """Height of Output Video

        Returns:
            int: height of video frame
        """
        return self._height

    @property
    def fps(self) -> float:
        """FPS of Output Video

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
    def ext(self) -> str:
        """Extension of Output Video

        Returns:
            str: ext of video
        """
        return self._ext

    @property
    def info(self) -> dict:
        """Video information

        Returns:
            dict: info of width, height, fps, backend and ext
        """
        return self._info

    @property
    def frame_count(self) -> int:
        """Total frames written

        Returns:
            int: written frames' count
        """
        return self._frame_count

    @property
    def seconds(self) -> float:
        """Total seconds written

        Returns:
            float: written frames' in seconds
        """
        return (self._frame_count / self._fps) if self._fps else 0

    @property
    def minutes(self) -> float:
        """Total minutes written

        Returns:
            float: written frames' in minutes
        """
        return self.seconds / 60.0

    def is_open(self) -> bool:
        """Checks if writer is still open

        Returns:
            bool: True if writer is open, False otherwise
        """
        return self._video_writer.isOpened()

    def write(self, frame: np.ndarray) -> None:
        """Write frame to output video

        Args:
            frame (np.ndarray): frame to write

        Raises:
            Exception: raised when method is called on a non-open writer.
        """
        # check if writer is open
        if not self.is_open():
            raise Exception(
                "[Vidsz-Error] Attempted writing with a non-open Writer.")

        self._video_writer.write(frame)
        self._frame_count += 1

    def write_all(self, frames: Union[List[np.ndarray], IReader]) -> None:
        """Write all frames to output video

        Args:
            frames (Union[List[np.ndarray], IReader]): Iterable object that contains frames.
        """
        for frame in frames:
            self.write(frame)

    def release(self) -> None:
        """Release Resources
        """
        if self._video_writer is not None:
            self._video_writer.release()

    def __del__(self) -> None:
        """Release Resources
        """
        self.release()
        self._video_writer = None

    def __repr__(self) -> str:
        """Writer's Info
        Returns:
            str: info
        """
        return str(self.info)

    def __str__(self) -> str:
        """Writer's Info
        Returns:
            str: info
        """
        return str(self.info)

    def __enter__(self) -> "Writer":
        """Returns Conext for "with" block usage
        Returns:
            Writer: Video Reader object
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
