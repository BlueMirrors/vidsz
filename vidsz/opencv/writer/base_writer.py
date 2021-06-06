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
