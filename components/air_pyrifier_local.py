#!/usr/bin/env python3

import socket
from helpers.air_helper import Airclient
from helpers.config import Config
from helpers.maps_util import Maps_util


class Air_pyrifier_local(Config):
    OPTIONS = ['name', 'pwr', 'temp', 'pm25', 'allergen', 'rh', 'rhset', 'func',
               'mode', 'fan', 'hepa_replace', 'carbon_replace', 'wick_replace']

    def __init__(self, host):
        self.host = Config.get_purifier_address()
        if host:
            self.host = host

        self.airclient = Airclient(socket.gethostbyname(self.host))

    def get(self, options):
        return self.airclient.get(options)

    def status(self):
        return self.get(Air_pyrifier_local.OPTIONS)

    def set(self, options):
        return self.airclient.set(Maps_util.list_to_dict(options))
