"""Benchmark and compare allocation strategy for numpy arrays.
This info is used in batch reading logic."""
import time
import argparse
import sys
import numpy as np


def pre_allocate(batch_size, height=720, width=1280):
    batch = np.zeros((batch_size, height, width, 3), dtype="uint8")

    for i in range(batch_size):
        batch[i] = np.zeros((height, width, 3))

    return batch


def dynamic_allocate(batch_size, height=720, width=1280):
    batch = []
    for _ in range(batch_size):
        batch.append(np.zeros((height, width, 3), dtype="uint8"))

    return np.array(batch)


def benchmark_allocate(iterations, batch_size):
    start = time.time()
    for _ in range(iterations):
        pre_allocate(batch_size)

    print("Time Taken (Pre-Allocate):", round(time.time() - start, 3))

    start = time.time()
    for _ in range(iterations):
        dynamic_allocate(batch_size)

    print("Time Taken (Dynamic-Allocate):", round(time.time() - start, 3))


def benchmark_reader_batch(iterations, batch_size):
    sys.path.insert(0, './')
    from vidsz.opencv import Reader
    fpath = "static/countdown.mp4"

    # batch
    start = time.time()
    for _ in range(iterations):
        with Reader(fpath, batch_size=batch_size) as reader:
            for frames in reader:
                continue
    
    print(f"Time taken (batch): ", round(time.time() - start, 3))

    # without-batch
    start = time.time()
    for _ in range(iterations):
        with Reader(fpath) as reader:
            for frame in reader:
                continue
    
    print(f"Time taken (non-batch): ", round(time.time() - start, 3))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-itrs", type=int, default=1000)
    parser.add_argument("-batch-size", type=int, default=64)
    parser.add_argument("-test-allocate", action="store_true")

    opt = parser.parse_args()
    if opt.test_allocate:
        benchmark_allocate(opt.itrs, opt.batch_size)
    else:
        benchmark_reader_batch(opt.itrs, opt.batch_size)
