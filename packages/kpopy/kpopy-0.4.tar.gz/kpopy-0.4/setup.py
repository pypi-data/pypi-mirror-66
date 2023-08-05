from setuptools import setup
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='kpopy',    # This is the name of your PyPI-package.
    version='0.4',                          # Update the version number for new releases
    #scripts=['kpackage'],
    author="Patrick Yoon",
    author_email="yoonpatrick3@gmail.com",
    description="KPop Api",
    long_description="Grab thousands of information about KPop artists. Check Github for documentation",
    url="https://github.com/yoonpatrick3/kpop-api",
    packages=['kpopy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)