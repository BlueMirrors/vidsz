import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(name="vidsz",
      version="0.2.0",
      description=
      "Common Wrapper/Interface around various video reading/writing tools",
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://github.com/BlueMirrors/vidsz",
      author="BlueMirrors",
      author_email="contact.bluemirrors@gmail.com",
      license="Apache Software License v2.0",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
      ],
      packages=find_packages(exclude=("test", )),
      install_requires=["opencv-python"])
