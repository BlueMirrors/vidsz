# Vidsz: Video's Wizard ![CI-Test-Status](https://github.com/BlueMirrors/vidsz/actions/workflows/ci_tests.yml/badge.svg)

Common Wrapper/Interface around various video reading/writing tools to make video reading stable, consistent and super easy around different systems and OS.

Backends

- OpenCV (in-development)

# Read Video

```
from vidsz import Reader

# open reader
reader = Reader("test.mp4")

# print info: width, height, fps etc.
print(reader)

# access specific things
print(reader.width, reader.height, reader.fps)

# access number-of-frames/seconds/minutes that have been read
print(reader.frame_count, reader.seconds, reader.minutes)

# read frames with while loop
while reader.is_open():
    # returns frame or None if nothing left to read
    frame = reader.read()

# read frame with for loop
for frame in reader:
    # use frame however you like
    pass

# release
reader.release()


# or read with a with block
with Reader("test.mp4") as reader:
    frame = reader.read()
    frames = reader.read_all() # list of frames returned
```

# Write Video

```
from vidsz import Reader, Writer

video_fname = "test.mp4"

# open reader
reader = Reader(video_fname)

# start writer with the Reader object
# by default it'll append _processed in file
writer = Writer(reader) name of reader's video name

# start writer with your settings;
# you can also give any combinations of
# following settings with Reader object to
# overwrite default settings
writer = Writer("out.mp4", width=680, height=340, fps=30)

# print writer info
print(writer)

# write frame
frame = reader.read()
writer.write(frame)

# close off
writer.release()
```
