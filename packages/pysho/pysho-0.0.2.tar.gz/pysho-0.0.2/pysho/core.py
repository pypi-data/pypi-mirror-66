import os
import sys
from .constants import WINDOWS, LINUX

# simple functions
from .funcs import call, capture, cd, cp, delete, grep, hr, ls, mkdir, start, touch

# generators and proxies
from .funcs import ENV, block

import logging

logging.root.setLevel(logging.INFO)
logging.root.name = "pysho"
