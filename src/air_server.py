#!/usr/bin/env python3
from helpers.air_helper import Airclient
import yaml
import socket
import asyncio
import websockets

import logging
logging.disable()


airpurifier = socket.gethostbyname('airpy.internal.suchanecki.me')
listenaddress = '0.0.0.0'
listenport = '8765'

ac = Airclient(airpurifier)


async def dispatcher(websocket, path):
    frame = await websocket.recv()
    payload = yaml.load(frame, Loader=yaml.BaseLoader)

    if payload['action'] == 'set':
        result = ac.set(payload['message'])  # nr of tries

    elif payload['action'] == 'get':
        result = ac.get(payload['message'])  # purifier data

    await websocket.send(yaml.dump(result))

start_server = websockets.serve(dispatcher, listenaddress, listenport)

print('starting server')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
del ac
