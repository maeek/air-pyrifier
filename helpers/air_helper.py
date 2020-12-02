import sys

from lib.coapair import CoAPAirClient
from helpers.maps_util import Maps_util

# map files config
int_requirement = 'int'
bool_requirement = 'bool'

missing_key = 'error'


class Airclient():
    def __init__(self, host):
        self.host = host

        # out = from mapped to org (going outside the airhelper to pyair)
        # in = from org to mapped (going inside from pyair to airhelper)
        self.options_map = Maps_util.get_options()
        self.values_map = Maps_util.get_values()

    # get status from air purifier
    # return dictionary of every option value
    # or one's specified in list
    def get(self, values=[]):
        """
        Gets status from air purifier

        @param values: list of attributes

        @returns: dictionary of every option value
        """
        self._connect()
        status = self._map_options('in', self.acli.get_status())

        if len(values) == 0:
            return status

        return_status = {}

        for value in values:
            try:
                return_status[value] = status[value]
            except KeyError:
                return_status[value] = missing_key

        return return_status

    def set(self, values={}):
        """
        Updates air purifier config

        @param values: list of options to update
        TODO: update
        """
        correct_values = self._map_options('out', values)

        # Try settings at least 5 times
        tries = 1
        while not self._set_values(correct_values):
            tries += 1
            if tries == 5:
                break

        return tries  # return number of tries

    def _map_options(self, direction, options):
        # TODO: move to maps util
        mapped_opts = {}
        for option in options:
            mapped_option = self._map_opt(direction, option)
            mapped_value = self._map_val(direction, option, options[option])

            if direction == 'out':
                # inside this script we operate on custom options ffs
                # mapped in this context means original ones due to
                # direction equal to 'out' (from script to pyair)
                mapped_value = self._check_value(option, mapped_value)

            mapped_opts[mapped_option] = mapped_value
        return mapped_opts

    # Some values needs to be string/int/bool
    #  it's air purifier requirement..

    def _check_value(self, option, value):
        requirement = self.options_map['out']['requirement'][option]
        if requirement == int_requirement:
            return int(value)
        elif requirement == bool_requirement:
            return bool(int(value))
        else:
            return str(value)

    # Useful helper because sometimes sending
    # data through CoAP won't work and recreating
    # client object is only solution

    def _set_values(self, values={}):
        self._connect()
        result = self.acli.set_values(values)
        del self.acli
        return result  # True/False (if setting data was successful)

    # Create CoAP connection to purifier
    # Sometimes sending requests gets buggy
    # and connection needs to be recreated
    # That's why set() is returning number of tries
    def _connect(self):
        self.acli = CoAPAirClient(self.host)

    # def map_opts(self, direction, opts):
    #     mapped_opts = {}
    #     for option in opts:
    #         mapped_opts[self._map_opt(direction, option)] = opts[option]
    #     return mapped_opts

    # mapped here does not mean the same as csv
    # mapped is according to {direction}

    def _map_opt(self, direction, opt):
        try:
            return self.options_map[direction][opt]
        except KeyError:
            return opt

    def _map_val(self, direction, option, value):
        try:
            return self.values_map[direction][option][value]
        except KeyError:
            return value
