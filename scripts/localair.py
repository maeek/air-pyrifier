#!/usr/bin/env python3

import os
import sys
import time
from airhelper import Airclient

ac = Airclient('10.20.0.200')

# Just convertings args to dictionary for helper


def list_to_dict(args):
    options = {}
    for index in range(len(args)):
        if index % 2 == 0:
            try:
                options[args[index]] = args[index+1]
            except IndexError:
                pass
    return options
# --------------


try:
    if sys.argv[1] == 'get':
        options = sys.argv[2:]
        result = ac.get(options)  # ac.get(list)

    # all of belows are working on ac.set(list->dict) or ac.get(list)
    elif sys.argv[1] == 'status':
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(ac.get(['name', 'pwr', 'temp', 'pm25', 'allergen', 'rh', 'rhset', 'func',
                          'mode', 'fan', 'hepa_replace', 'carbon_replace', 'wick_replace']))
        result = 0

    elif sys.argv[1] == 'version':
        result = '2'

    else:  # sys.argv[1] in ['name','rhset','pwr','cl','mode','hud','ring','menu']:
        args = sys.argv[1:]
        result = ac.set(list_to_dict(args))  # ac.set(dict)

    print(result)

except IndexError:
    print(f'Usage:\n{os.path.basename(__file__)} get [option] [option2]..')
    print(f'{os.path.basename(__file__)} option value option2 value2..')
    print(f'{os.path.basename(__file__)} status')
    print(f'\nAvailable options:')
    print(f' name\t\t[hostname]')
    print(f' pwr\t\t0/1')
    print(f' cl\t\t0/1')
    print(f' mode\t\tauto/sleep/allergen')
    print(f' hud\t\tiai/pm25/gas/humidity')
    print(f' ring\t\t0/25/50/75/100')
    print(f' menu\t\t0/1')
    print(f' rhset\t\t40/50/60/70')
    print(f' fan\t\ts/1/2/3/t')
    print(f' func\t\tp/ph')

del ac
