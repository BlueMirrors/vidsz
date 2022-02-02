"""Benchmark and compare allocation strategy for numpy arrays.
This info is used in batch reading logic."""
import time
import argparse
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


def benchmark(iterations, batch_size):
    start = time.time()
    for _ in range(iterations):
        pre_allocate(batch_size)

    print("Time Taken (Pre-Allocate):", round(time.time() - start, 3))

    start = time.time()
    for _ in range(iterations):
        dynamic_allocate(batch_size)

    print("Time Taken (Dynamic-Allocate):", round(time.time() - start, 3))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-itrs", type=int, default=1000)
    parser.add_argument("-batch-size", type=int, default=64)

    opt = parser.parse_args()
    benchmark(opt.itrs, opt.batch_size)
