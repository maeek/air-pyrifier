#!/usr/bin/env python3

import os
import sys
import time
import yaml
from websocket import create_connection

airserver = 'ws://172.17.0.2:8765'
ws = create_connection(airserver)

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

def send_to_server(ws,action,message):
  payload = yaml.dump({'action':action,'message':message})
  ws.send(payload)
  return yaml.load(ws.recv(),Loader=yaml.BaseLoader)

try:
  # if sys.argv[1] == 'set':
  #   args = sys.argv[2:]
  #   result = send_to_server(ws,'set',list_to_dict(args))

  # el
  if sys.argv[1] == 'get':
    options = sys.argv[2:]
    result = send_to_server(ws,'get',options)

  # all of belows are working on air_set(list->dict) or ac.get(list)
  elif sys.argv[1] == 'status':
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(send_to_server(ws,'get',['name','pwr','temp','pm25','allergen','rh','rhset','func','mode','fan','hepa_replace','carbon_replace','wick_replace']))
    result = 0

  elif sys.argv[1] == 'version':
    result = '2'
  
  else:# sys.argv[1] in ['name','rhset','pwr','cl','mode','hud','ring','menu']:
    args = sys.argv[1:]
    result = send_to_server(ws,'set',list_to_dict(args))

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

ws.close()
