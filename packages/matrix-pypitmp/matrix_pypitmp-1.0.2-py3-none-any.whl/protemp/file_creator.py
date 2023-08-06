"""Interact with the Real Python feed"""
# Standard library imports
import os

# Third party imports

# Reader imports


# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

def fwriter(project_name=None,read_file=None,write_file=None,write_path=None):
    #to read and replace files
    with open(os.path.join(HERE, read_file)) as rid:
        readtxt = rid.read()
    readtxt.replace("protemp", project_name)
    with open(os.path.join(write_path, write_file), "w+") as wid:
        README = wid.write(readtxt)


def get_projectname(project_name="matrix_template",path_to_proj=os.getcwd()):
    project_root_path = os.path.join(path_to_proj,project_name+"_root")
    project_files_path = os.path.join(path_to_proj,project_name+"_root",project_name)
    if os.path.isdir(project_root_path):
        print("Project Folder Already Exists..")
        return -1
    os.mkdir(project_root_path)
    print('Project root folder created at ...',project_root_path)
    os.mkdir(project_files_path)
    print('Project files folder created at ...',project_files_path)
    fwriter(project_name=project_name,read_file="init_r.py",write_file="__init__.py",write_path=project_files_path)
    fwriter(project_name=project_name,read_file="main_r.py",write_file="__main__.py",write_path=project_files_path)
    fwriter(project_name=project_name,read_file="config_r.py",write_file="config.cfg",write_path=project_files_path)
    fwriter(project_name=project_name,read_file="p_imp1_r.py",write_file="your_python_file.py",write_path=project_files_path)
    fwriter(project_name=project_name,read_file="helper_r.py",write_file="helper.py",write_path=project_files_path)
    print('Project file templates created')
    fwriter(project_name=project_name,read_file="MANIFEST_r.py",write_file="MANIFEST.in",write_path=project_root_path)
    fwriter(project_name=project_name,read_file="README_r.py",write_file="README.md",write_path=project_root_path)
    fwriter(project_name=project_name,read_file="setup_r.py",write_file="setup.py",write_path=project_root_path)
    print('Other Essential Files Created')
    return print("Templated Successfully Created")