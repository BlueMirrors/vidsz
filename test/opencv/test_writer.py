"""Test Base Writer's behavior and correctness.
"""
import os
import sys

sys.path.insert(0, './')

import pytest
import numpy as np
from vidsz.opencv import (Reader, Writer)

VIDEO_PATHS = ['static/countdown.mp4']


@pytest.mark.parametrize("vpath", VIDEO_PATHS)
def test_correctness(vpath: str) -> None:
    """Test Reader correctness by writing and then reading the video.

    Args:
        vpath (str): path to video
    """
    # open reader
    reader = Reader(vpath)
    frame = reader.read()

    # opencv cv reader
    writer = Writer(reader)
    writer.write(frame)

    # write all the frames
    writer.write_all(reader)

    # print info: width, height, fps etc.
    assert str(writer), "Representation not clear"

    # try access specific things
    print('Info:', writer.width, writer.height, writer.fps)

    # access number-of-frames/seconds/minutes that have been read
    print('Status: ', writer.frame_count, writer.seconds, writer.minutes)

    # release resources
    writer.release()
    reader.release()

    # check the written file is proper
    new_reader = Reader(writer.name)
    assert new_reader.is_open(), "Failed to Write File."
    assert np.array_equal(frame.shape,
                          new_reader.read().shape), "Failed to Properly Write"
    new_reader.release()

    # delete file
    os.remove(writer.name)


@pytest.mark.parametrize("vpath", VIDEO_PATHS)
def test_with_overwriting_configs(vpath: str) -> None:
    """Test Writer's feature of overwriting configs

    Args:
        vpath (str): path to video
    """
    with Reader(vpath) as reader:
        with Writer(reader, name='temp.mp4', fps=10) as writer:
            writer.write_all(reader)
            assert writer.name == 'temp.mp4', "Failed to overwrite name"
            assert writer.fps == 10, "Failed to overwrite FPS"

    with Reader("temp.mp4") as reader:
        assert reader.fps == 10, "Failed to overwrite FPS"
    os.remove('temp.mp4')


def test_exceptions() -> None:
    """Test if writer raises correct exceptions when needed
    """
    # create without reader or name
    exception_flag = False
    try:
        writer1 = Writer()
        print(writer1)
        writer1.release()

    except AssertionError as _:
        exception_flag = True

    assert exception_flag, "Failed to raise proper exception."

    # create with unsupported ext
    exception_flag = False
    try:
        writer2 = Writer(name='test', ext='jst')
        print(writer2)
        writer2.release()

    except NotImplementedError as _:
        exception_flag = True

    assert exception_flag, "Failed to raise proper exception."


@pytest.mark.parametrize("vpath", VIDEO_PATHS)
def test_writer_after_release(vpath: str) -> None:
    """Test Writer behavior after release operation.

    Args:
        vpath (str): path to video
    """
    print("Test After Release")

    # init reader and writer
    reader = Reader(vpath)
    writer = Writer(reader, name='temp.mp4')
    while reader.is_open():
        # dummy read (for 10 times)
        frame = reader.read()

        # check if valid frame (required behavior for using `while` block)
        if frame is not None:
            writer.write(frame)

        # release and test behavior
        if reader.frame_count > 10:
            print("Releasing...")
            writer.release()

            # sholud throw exception
            frame = reader.read()
            if frame is not None:
                # TODO: catch custom exception
                with pytest.raises(Exception) as execinfo:
                    writer.write(frame)

                # check if correct exception was raised
                expected_error = "[Vidsz-Error] Attempted writing with a non-open Writer."
                assert str(execinfo.value) == expected_error

            # access writer properties, even after release
            print(writer)

            # release reader
            reader.release()

    # check written frame count
    assert writer.frame_count == 11, "expected frame count doesn't match"

    # clean up
    os.remove('temp.mp4')
