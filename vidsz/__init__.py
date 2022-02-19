"""Common Wrapper/Interface around various video reading/writing tools to make video reading stable,
consistent and super easy around different systems and OS.

Backends
    - OpenCV (in-development)

# How to Read Video
```python

    from vidsz import Reader

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

```

# How to Write Video

```python

    from vidsz import Reader, Writer

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
    writer = Writer("out.mp4", width=680, height=340, fps=30, ext="avi")

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
        with Writer(reader) as writer:
            writer.write_all(reader)
```
"""
__version__ = "0.2.0"
