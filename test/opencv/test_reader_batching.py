"""Test Base Reader's behavior and correctness with batching.
"""
import sys

sys.path.insert(0, './')

import pytest
import cv2
import numpy as np
from vidsz.opencv import Reader

VIDEO_PATHS = ['static/countdown.mp4']
BATCH_SIZES = [2, 4, 8, 16, 32, 64]


@pytest.mark.parametrize("vpath", VIDEO_PATHS)
@pytest.mark.parametrize("batch_size", BATCH_SIZES)
def test_correctness(vpath: str, batch_size: int) -> None:
    """Test Reader correctness by comparing with OpenCV Reader
    (static-batching)

    Args:
        vpath (str): path to video
    """
    # open reader
    reader = Reader(vpath, batch_size=batch_size)

    # opencv cv reader
    cv2_reader = cv2.VideoCapture(vpath)

    width = int(cv2_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cv2_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    expected_shape = (batch_size, height, width, 3)

    count = 0
    for batch in reader:

        assert batch.shape == expected_shape, "Batch Shape doesn't match"

        for frame in batch:
            count += 1

            # no more frames to match
            if count > reader.frame_count:
                break

            cv2_frame = cv2_reader.read()[1]
            assert np.array_equal(cv2_frame, frame), "Frame Don't Match."

    assert not cv2_reader.read()[0], "All frames were not read."

    cv2_reader.release()
    reader.release()


@pytest.mark.parametrize("vpath", VIDEO_PATHS)
@pytest.mark.parametrize("batch_size", BATCH_SIZES)
def test_correctness_dynamic(vpath: str, batch_size: int) -> None:
    """Test Reader correctness by comparing with OpenCV Reader
    (dynamic batching)

    Args:
        vpath (str): path to video
    """
    # open reader
    reader = Reader(vpath, batch_size=batch_size, dynamic_batch=True)

    # opencv cv reader
    cv2_reader = cv2.VideoCapture(vpath)
    width = int(cv2_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cv2_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    expected_shape = (height, width, 3)

    for batch in reader:

        assert len(batch.shape) == 4, "Batch axis count does not match."
        assert batch.shape[1:] == expected_shape, "Batch Shape doesn't match"

        for frame in batch:
            cv2_frame = cv2_reader.read()[1]
            assert np.array_equal(
                cv2_frame,
                frame), f"{reader.frame_count}th Frame doesn't Match."

    assert not cv2_reader.read()[0], "All frames were not read."

    cv2_reader.release()
    reader.release()
