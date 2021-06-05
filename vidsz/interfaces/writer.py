import abc


class _IWriter(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def name(self):
        ...

    @property
    @abc.abstractmethod
    def width(self):
        ...

    @property
    @abc.abstractmethod
    def height(self):
        ...

    @property
    @abc.abstractmethod
    def fps(self):
        ...

    @property
    @abc.abstractmethod
    def backend(self):
        ...

    @property
    @abc.abstractmethod
    def ext(self):
        ...

    @property
    @abc.abstractmethod
    def info(self):
        ...

    @property
    @abc.abstractmethod
    def frame_count(self):
        ...

    @property
    @abc.abstractmethod
    def seconds(self):
        ...

    @property
    @abc.abstractmethod
    def minutes(self):
        ...

    @abc.abstractmethod
    def is_open(self):
        ...

    @abc.abstractmethod
    def write(self):
        ...

    @abc.abstractmethod
    def write_all(self):
        ...

    @abc.abstractmethod
    def release(self):
        ...

    @abc.abstractmethod
    def __del__(self):
        ...

    @abc.abstractmethod
    def __repr__(self):
        ...

    @abc.abstractmethod
    def __str__(self):
        ...

    @abc.abstractmethod
    def __enter__(self):
        ...

    @abc.abstractmethod
    def __exit__(self):
        ...
