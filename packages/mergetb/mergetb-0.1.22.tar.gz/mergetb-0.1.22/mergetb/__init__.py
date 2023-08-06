'''
mergetb is a python interface to the MergeTB API.
'''

# pylint: disable=wildcard-import
# OK in this case as we want everything in lib in the mergetb namespace.
from .lib import *
from .auth import login, logout
from .cli import request_token
