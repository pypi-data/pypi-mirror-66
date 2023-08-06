"""Setup script for your-project"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="Project_Name_To_Publish",
    version="1.0.0",
    description="Enter a Short description Here",
    long_description=README,
    long_description_content_type="text/markdown",
    url="your-project_url_here",
    author="Your_NAME_Obviously",
    author_email="trixter127@pm.me",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["reader"],
    include_package_data=True,
    install_requires=[
        "add", "your", "external", "imports","Here"
    ],
    entry_points={"console_scripts": ["mtrxtmp=protemp.__main__:main"]},
)
# This entry_points is what you want to use console 
#and what file and function to call