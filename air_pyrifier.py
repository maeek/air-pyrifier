#!/usr/bin/env python3

import json
import os
import pprint
import sys
import time
from air_pyrifier_server import Air_pyrifier_server
from air_pyrifier_client import Air_pyrifier_client

pp = pprint.PrettyPrinter(indent=4)

VERSION = '1.0.0'

try:
    if sys.argv[1] == 'listen':
        Air_pyrifier_server().run()

    elif sys.argv[1] == 'get':
        options = sys.argv[2:]
        results = Air_pyrifier_client().get(options)

        pp.pprint(results)

    # # all of belows are working on air_set(list->dict) or ac.get(list)
    elif sys.argv[1] == 'status':
        results = Air_pyrifier_client().status()

        pp.pprint(results)

    elif sys.argv[1] == 'version':
        result = VERSION

    else:  # sys.argv[1] in ['name','rhset','pwr','cl','mode','hud','ring','menu']:
        options = sys.argv[1:]
        results = Air_pyrifier_client().set(options)

        pp.pprint(results)

except IndexError:
    print('Usage: air-pyifier.py listen')
