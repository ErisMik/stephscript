"""
StephScript Main
"""

import os
import sys
from stephscript.compiler import *

def main():
    """
    Main program loop
    """
    if len(sys.argv) != 2:
        print("Invalid usage. Provide a StephScript file name to compile and run")
        print("Example: python main.py steph_file.stsc")
        return

    if not os.path.isfile(sys.argv[1]):
        print("Invalid file specified")
        return

    # Compile and run
    Compiler().compile(sys.argv[1])

if __name__ == "__main__":
    main()
