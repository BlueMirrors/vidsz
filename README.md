# <img src="https://raw.githubusercontent.com/BlueMirrors/vidsz/master/static/logo.png" width="30">Vidsz: Video's Wizard

![CI-Test-Status](https://github.com/BlueMirrors/vidsz/actions/workflows/ci_tests.yml/badge.svg) [![CodeFactor](https://www.codefactor.io/repository/github/bluemirrors/vidsz/badge?s=8752aa2850f09145fc469fd9a07eafb5144d56fc)](https://www.codefactor.io/repository/github/bluemirrors/vidsz) ![status](https://img.shields.io/pypi/status/ansicolortags.svg) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Documentation Status](https://readthedocs.org/projects/vidsz/badge/?version=latest)](https://vidsz.readthedocs.io/en/latest/?badge=latest) [![Downloads](https://static.pepy.tech/personalized-badge/vidsz?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/vidsz)

Common Wrapper/Interface around various video reading/writing tools to make video reading stable, consistent and super easy around different systems and OS.

```bash
pip install vidsz
```

Backends

- OpenCV (in-development)


Features

- Easy and hassle free (read/write with ```for-loop```, ```with-block```, ```while-loop```)
- Batch Support. Read and write frames in batches.


# Read Video


## Read with ```for-loop```
```python
from vidsz.opencv import Reader

# open reader
reader = Reader("static/countdown.mp4")

# read frame with for loop
for frame in reader:
    # use ndarry-frame however you like
    pass

# release
reader.release()
```


## Read with a ```with-block```
```python
with Reader("static/countdown.mp4") as reader:
    frame = reader.read()
```


## Read with a ```while-loop```
```python
# this follows similar behavior as opencv counterpart
while reader.is_open():
    # returns ndarry-frame or None if nothing left to read
    frame = reader.read()
    if frame is None:
        break
```


## Read frames in a ```batch```
```python
with Reader("dummy.mp4", batch_size=8, dynamic_batch=True) as reader:
    batch_frames = reader.read()
```


## Get properties of the reader
```python
# print info: width, height, fps etc.
print(reader)

# access specific things
print(reader.width, reader.height, reader.fps)

# access number-of-frames/seconds/minutes that have been read
print(reader.frame_count, reader.seconds, reader.minutes)
```


# Write Video


## Write a single frame
```python
from vidsz.opencv import Reader, Writer

video_fname = "static/countdown.mp4"

# open reader
reader = Reader(video_fname)

# start writer with the Reader object
# by default it'll append _out in the name of the output video
writer = Writer(reader)

# start writer with your settings;
# you can also give any combinations of
# following settings with Reader object to
# overwrite default settings
writer = Writer(name="out.mp4", width=1920, height=1080, fps=15)

# print writer info
print(writer)

# write single frame
frame = reader.read()
writer.write(frame)
```


## Write with ```for-loop```
```python
# read frame with for loop
for frame in reader:
    # write the ndarry-frame
    writer.write(frame)
```


## Write a ```batch```
```python
# read batches and write
with Reader("dummy.mp4", batch_size=8, dynamic_batch=True) as reader:
    batch_frames = reader.read()
    # write list or ndarray of frames
    writer.write_all(batch_frames)

# close off
reader.release()
writer.release()
```


## Write with a ```with-block```
```python
# using "with" block, write "static/countdown_out.mp4" (clone of input)
with Reader(video_fname) as reader:
    with Writer(reader, name="out_with.mp4") as writer:
        writer.write_all(reader)
```

***Logo-Attribution***
<a href="http://www.freepik.com">Designed by brgfx / Freepik</a>
