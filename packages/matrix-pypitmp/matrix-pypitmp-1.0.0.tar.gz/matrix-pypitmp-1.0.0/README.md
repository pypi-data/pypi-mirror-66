
# Matrix  PyPI Package Template 

The Matrix  PyPI Package Template is a basic template project creator uploading your project to PyPi packages index and make it globally available to the whole python community 


## Installation

You can install the Matrix  PyPI Package Template from [PyPI](https://pypi.org/project/matrix-pypitmp/):

    pip install matrix-pypitmp

The package is supported on Python 2.7, as well as Python 3 and above.

## How to use

The Matrix  PyPI Package Template is a command line application, named `mtrxtmp`. To create a template for your package to upload in pypi index simply call the program by specifying your project name and path to create it :

    $ mtrxtmp [options] args ...
Specify the project name and  path  you want to create it

    optional arguments:
    -h, --help            show this help message and exit
    --name PROJECT_NAME, 
	-n PROJECT_NAME  	  Name of the Project 
    --path PATH, -p PATH  Path to project template to be created
Example :
   
    $mtrxtmp --name PROJECT_NAME --path "/PATH/TO/CREATE/PROJECT"
   Running the program without an argument creates a project template with default name('matrix-pypi-template')  in current working directory 
