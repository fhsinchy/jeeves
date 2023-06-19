import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="jeeves",
    version="0.0.2",
    description=" Docker based development-only dependency manager for Windows, Linux, and macOS",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/fhsinchy/jeeves",
    author="Farhan Hasin Chowdhury",
    author_email="shovik.is.here@gmail.com",
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GPL-3.0 License",
        "Programming Language :: Python :: 3",
    ],
    py_modules=["data", "jeeves"],
    entry_points={"console_scripts": ["jeeves=jeeves:jeeves"]},
    install_requires=[
        'click',
        'docker'
    ],
)
