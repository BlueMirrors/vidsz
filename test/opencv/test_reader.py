"""Test Base Reader's behavior and correctness.
"""
import sys

sys.path.insert(0, './')

import pytest
import cv2
import numpy as np
from vidsz.opencv import Reader

VIDEO_PATHS = ['static/countdown.mp4']


@pytest.mark.parametrize("vpath", VIDEO_PATHS)
def test_correctness(vpath: str) -> None:
    """Test Reader correctness by comparing with OpenCV Reader

    Args:
        vpath (str): path to video
    """
    # open reader
    reader = Reader(vpath)

    # opencv cv reader
    cv2_reader = cv2.VideoCapture(vpath)

    for frame in reader:
        assert np.array_equal(frame,
                              cv2_reader.read()[1]), "Frame Don't Match."

    assert not cv2_reader.read()[0], "All frames were not read."

    cv2_reader.release()
    reader.release()


@pytest.mark.parametrize("vpath", VIDEO_PATHS)
def test_state(vpath: str) -> None:
    """Test Reader's properties' behavior

    Args:
        vpath (str): path to video
    """
    # open reader
    reader = Reader(vpath)

    # print info: width, height, fps etc.
    assert str(reader), "Representation not clear"

    # try access specific things
    print('Info:', reader.width, reader.height, reader.fps)

    # access number-of-frames/seconds/minutes that have been read
    print('Status: ', reader.frame_count, reader.seconds, reader.minutes)

    # release
    reader.release()


@pytest.mark.parametrize("vpath", VIDEO_PATHS)
def test_while_loop(vpath: str) -> None:
    """Test Reader behavior with while loop.

    Args:
        vpath (str): path to video
    """
    # open reader
    reader = Reader(vpath)

    # last frame count
    last = 0

    # read frames with while loop
    print("Reading with While Loop")
    while reader.is_open():
        # returns frame or None if nothing left to read
        frame = reader.read()
        if frame is None:
            break
        if reader.frame_count % 50 == 0:
            print(reader.seconds)
        if last == reader.frame_count:
            assert False, "Frame Count Not Changing after read..."
        last = reader.frame_count
    reader.release()


@pytest.mark.parametrize("vpath", VIDEO_PATHS)
def test_for_loop(vpath: str) -> None:
    """Test Reader behavior with for loop.

    Args:
        vpath (str): path to video
    """
    # open reader
    reader = Reader(vpath)

    # read frame with for loop
    print("Reading with For Loop")
    for frame in reader:
        assert frame is not None, "Loop Reading None Frames."
        if reader.frame_count % 50 == 0:
            print(reader.seconds)

    # release
    reader.release()


@pytest.mark.parametrize("vpath", VIDEO_PATHS)
def test_with_all(vpath: str) -> None:
    """Test Reader behavior with 'with' block.

    Args:
        vpath (str): path to video
    """
    # or read with a with block
    with Reader(vpath) as reader:
        frames = reader.read_all()  # list of frames returned

        assert all(frame is not None for frame in frames), "Bad Frame Read"
