"""Create a Template folder to upload in pypi 

Usage:
------

    $ mtrxtmp [options] [args]



Available options are:

    -h, --help         Show this help
    -n, --proj-name    name of your project
    -p, --path         path to your projext


Contact:
--------

More information is available at:

- https://pypi.org/project/matrix-pypitmp/
- https://github.com/mohankumarpaluru/matrix-pypitmp


Version:
--------

- matrix-pypitmp v1.0.0
"""
# Standard library imports
import os
import sys
import argparse

# Reader imports
from protemp
from protemp import file_creator as fc



def main():  # type: () -> None

    CWD = os.path.abspath(os.getcwd())
    parser = argparse.ArgumentParser(prog='mtrxtmp',
                                    usage='%(prog)s [-n] project_name [-p] path ',
                                    description='Specify the path and project name you want to create ')
    parser.add_argument(
      '--name',
      '-n',
      type=str,
      default='matrix-pypi-template',
      help='Name of your Project'
    )  
    parser.add_argument(
      '--path',
      '-p',
      type=str,
      default=CWD,
      help='Path to project template to be created'
    )

    args = parser.parse_args()
    arg_dict = vars(args)
    # print(arg_dict)
    project_name = args.name
    path = os.path.abspath(args.path)
    if path.count('\"') == 1 :
        path = path.replace("\"","")
    if not os.path.isdir(path):
         print('The path specified does not exist')
         sys.exit()
    fc.get_projectname(project_name=project_name,path_to_proj=path)

if __name__ == "__main__":
    main()
