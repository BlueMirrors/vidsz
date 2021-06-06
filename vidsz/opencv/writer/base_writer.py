import os
from typing import Optional

from vidsz.interfaces import _IWriter
from vidsz.interfaces import _IReader


class Writer(_IWriter):
    _EXT_TO_FOURCC = {".avi": "DIVX", ".mkv": "X264", ".mp4": "mp4v"}

    def __init__(self,
                 reader: Optional[_IReader] = None,
                 name: Optional[str] = None,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 fps: Optional[int] = None,
                 ext: Optional[str] = None) -> None:

        # initiate props
        self._initiate_props()

        # update props if provided
        self._update_props(reader, name, width, height, fps, ext)

        # initiate writer
        self._video_writer = cv2.VideoWriter(self._name, self._fourcc(),
                                             self._fps,
                                             (self._width, self._height))

        # check if open
        self._is_open = self._video_writer.isOpened()

        if not self.is_open():
            raise "Failed to Create Writer for the given settings."

    def _initiate_props(self) -> None:
        """Initiate all class properties to default values
        """
        self._name = None
        self._is_open = False
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
                      reader: Optional[_IReader] = None,
                      name: Optional[str] = None,
                      width: Optional[int] = None,
                      height: Optional[int] = None,
                      fps: Optional[int] = None,
                      ext: Optional[str] = None) -> None:

        # set default if given
        if reader is not None:
            reader_name, reader_ext = os.path.splitext(reader.name)[0]
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
            raise Exception("Must provide either Reader or name arg.")

        # set ext for CV2 writer creations
        self._ext = os.path.splitext(self._name)[1] if ext is None else ext

        # add . for consistency
        if '.' not in self._ext:
            self._ext = '.' + self._ext

    def _update_info(self):
        """Update info property according to props
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

    def _fourcc(self):
        if self._ext not in self._EXT_TO_FOURCC:
            raise NotImplemented
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
        """Width of Video

        Returns:
            int: width of video frame
        """
        return self._width

    @property
    def height(self):
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
    def ext(self) -> str:
        """Name of the ext being used

        Returns:
            str: current ext
        """
        return self._ext

    @property
    def info(self) -> dict:
        """Video Informations

        Returns:
            dict: info of width, height, fps and backend.
        """
        return self._info

    @property
    def frame_count(self) -> int:
        """Number of frames already been written

        Returns:
            int: written frames' count
        """
        return self._frame_count

    @property
    def seconds(self) -> float:
        """Amount of seconds already been written

        Returns:
            float: written frames' in seconds
        """
        return (self._frame_count / self._fps) if self._fps else 0

    @property
    def minutes(self) -> float:
        """Amount of minutes already been written

        Returns:
            float: written frames' in minutes
        """
        return self.seconds / 60.0
