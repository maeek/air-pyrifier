#!/usr/bin/env python3
from helpers.run_util import Run_util
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

# VERSION = '1.0.0'

try:
    pp.pprint(Run_util.dispatcher(sys.argv[1], sys.argv[2:]))

except IndexError:
    print('Usage: air-pyifier.py listen')
