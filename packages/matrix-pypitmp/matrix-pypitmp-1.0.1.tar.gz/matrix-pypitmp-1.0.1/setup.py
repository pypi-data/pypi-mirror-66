"""Setup script for realpython-reader"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="matrix-pypitmp",
    version="1.0.1",
    description="Create a template for pypi repo",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mohankumarpaluru/matrix-pypitmp",
    author="Mohan Kumar Paluru",
    author_email="trixter127@pm.me",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["protemp"],
    include_package_data=True,
    install_requires=[
        "wheel","twine"
    ],
    entry_points={"console_scripts": ["mtrxtmp=protemp.__main__:main"]},
)
