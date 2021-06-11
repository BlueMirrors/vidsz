# <img src="https://github.com/BlueMirrors/vidsz/blob/master/static/logo.png" width="30">Vidsz: Video's Wizard 
![CI-Test-Status](https://github.com/BlueMirrors/vidsz/actions/workflows/ci_tests.yml/badge.svg) [![CodeFactor](https://www.codefactor.io/repository/github/bluemirrors/vidsz/badge?s=8752aa2850f09145fc469fd9a07eafb5144d56fc)](https://www.codefactor.io/repository/github/bluemirrors/vidsz) ![status](https://img.shields.io/pypi/status/ansicolortags.svg) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Documentation Status](https://readthedocs.org/projects/vidsz/badge/?version=latest)](https://vidsz.readthedocs.io/en/latest/?badge=latest)

Common Wrapper/Interface around various video reading/writing tools to make video reading stable, consistent and super easy around different systems and OS.

```bash
pip install vidsz
```

Backends

- OpenCV (in-development)

# Read Video

```python
from vidsz.opencv import Reader

# open reader
reader = Reader("static/countdown.mp4")

# print info: width, height, fps etc.
print(reader)

# access specific things
print(reader.width, reader.height, reader.fps)

# access number-of-frames/seconds/minutes that have been read
print(reader.frame_count, reader.seconds, reader.minutes)

# read frames with while loop
while reader.is_open():
    # returns ndarry-frame or None if nothing left to read
    frame = reader.read()

# read frame with for loop
for frame in reader:
    # use frame however you like
    pass

# release
reader.release()


# or read with a with block
with Reader("static/countdown.mp4") as reader:
    frame = reader.read()
    frames = reader.read_all() # list of frames returned
```

# Write Video

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

# write list of frames 
# or directly write everything from reader object
writer.write_all(reader)

# close off
writer.release()

# using "with" block, write "static/countdown_out.mp4" (clone of input)
with Reader(video_fname) as reader:
    with Writer(reader, name="out_with.mp4") as writer:
        writer.write_all(reader)
```

***Logo-Attribution***
<a href="http://www.freepik.com">Designed by brgfx / Freepik</a>
