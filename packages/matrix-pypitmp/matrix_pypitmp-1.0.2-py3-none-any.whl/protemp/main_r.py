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
import sys

# Reader imports
import protemp
from protemp import helper
from protemp import your_python_file



def main():  # type: () -> None
    """Read the Real Python article feed"""
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    # Show help message
    if "-h" in opts or "--help" in opts:
        helper.show(__doc__)
        return

    
    if args:
        #do some stuff here
        pass
 
    else:
        helper.show(__doc__)
        return

if __name__ == "__main__":
    main()
