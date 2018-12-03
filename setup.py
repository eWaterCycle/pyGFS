import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyGFS",
    version="0.0.1",
    author="Ronald van Haren",
    author_email="r.vanharen@esciencecenter.nl",
    description=("A python library to download weather forecasts from "
                 "the Global Forecast System (GFS)."),
    license="Apache 2.0",
    keywords="GFS",
    url="https://github.com/ewatercycle/pyGFS",
    packages=['pygfs'],
    include_package_data=False,    # include everything in source control
    scripts=['pygfs/scripts/pygfs'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=['requests', 'configargparse'],
)
