#!/usr/bin/env python3

import os
import sys
import time
import yaml
from websocket import create_connection
from helpers.config import Config
from helpers.maps_util import Maps_util


class Air_pyrifier_client(Config):
    OPTIONS = ['name', 'pwr', 'temp', 'pm25', 'allergen', 'rh',
               'rhset', 'func', 'mode', 'fan', 'hepa_replace',
               'carbon_replace', 'wick_replace']

    def __init__(self):
        self.airserver_ws_address = Config.get_server_ws_address()
        self.airserver_ws_port = Config.get_server_listen_port()

    def connect(self):
        self.ws = create_connection(f'ws://{self.airserver_ws_address}:{self.airserver_ws_port}')

    def disconnect(self):
        self.ws.close()

    def get(self, options):
        self.connect()

        results = self._send_to_server('get', options)

        self.disconnect()

        return results

    def set(self, options):
        self.connect()

        results = self._send_to_server('set', Maps_util.list_to_dict(options))

        self.disconnect()

        return results

    def status(self):
        self.connect()

        results = self._send_to_server('get', Air_pyrifier_client.OPTIONS)

        self.disconnect()

        return results

    def _send_to_server(self, action, message):
        payload = yaml.dump({'action': action, 'message': message})
        self.ws.send(payload)
        return yaml.load(self.ws.recv(), Loader=yaml.BaseLoader)
