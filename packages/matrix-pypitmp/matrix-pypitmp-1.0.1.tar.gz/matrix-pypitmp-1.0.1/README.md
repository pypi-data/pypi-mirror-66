
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

The use of this package ends here.Now if your want to publish your package to pypi, follow the below steps:
Requirements : 

	setuptools wheel twine
Once the Project Template is adjusted to suit your project what needs to be done next is building your python package, It can be done by entering the following command in your project root directory :

	$python setup.py sdist bdist_wheel

That should generate a build , dist and an egg for your project. To verify all the formats are correct we use a package called [twine](https://pypi.org/project/twine/) as below from your root directory:

	$twine check dist/*
Now we have everything ready for our package upload :) .But.. we never tested how our newly created package works, so we upload to pypi test server to test and then upload to the actual one.
To do that :

	$twine upload --repository testpypi dist/*
This will ask for your test pypi username and password to upload
Once this is done you have your package ready to test from test pypi server and can be installed with 

	$pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-YOUR-USERNAME-HERE

Now you can test your package and make any adjustments if needed and upload to pypi by making a new dist if required.
To uplaod into actual pypi repository all you need to do is enter the following command in your adjusted projects root folder

	$twine  upload  dist/*	
It will ask for your pypi username and password to upload and you are done
you can check your package in 
https://pypi.org/project/YOUR_PACKAGE-NAME-HERE/

for more detailed  guide on packaging your project and uploading check [Python's Official Guide on Packaging](https://packaging.python.org/tutorials/packaging-projects/)
	
