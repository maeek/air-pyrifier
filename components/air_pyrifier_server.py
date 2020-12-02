#!/usr/bin/env python3
from helpers.air_helper import Airclient
from helpers.config import Config
import yaml
import socket
import asyncio
import websockets
import logging


logging.disable()


class Air_pyrifier_server(Config):
    def __init__(self):
        self.host = socket.gethostbyname(Config.get_purifier_address())
        self.listenaddress = Config.get_server_listen_address()
        self.listenport = Config.get_server_listen_port()
        self.airclient = Airclient(self.host)

    def listen(self):
        self.server = websockets.serve(self._dispatcher, self.listenaddress, self.listenport)

        print('starting server')

        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    async def _dispatcher(self, websocket, path):
        frame = await websocket.recv()
        payload = yaml.load(frame, Loader=yaml.BaseLoader)

        if payload['action'] == 'set':
            result = self.airclient.set(payload['message'])  # nr of tries

        elif payload['action'] == 'get':
            result = self.airclient.get(payload['message'])  # purifier data

        await websocket.send(yaml.dump(result))
