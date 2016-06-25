"""
Contains a set of utilities related to system paths.
"""
import os, sys

def selfpath():
    """
    Returns the abs path of the file, regardless of where it is called from.
    """
    return os.path.dirname(os.path.realpath(sys.argv[0]))

