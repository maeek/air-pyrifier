import sys

from lib.coapair import CoAPAirClient

# map files location
options_map_file = f'{sys.path[0]}/resources/options.map'
values_map_file = f'{sys.path[0]}/resources/values.map'

# map files config
csv_indicator = ';'
int_requirement = 'int'
bool_requirement = 'bool'

missing_key = 'error: missing key'


class Airclient():
    def __init__(self, host):
        self.host = host

        # out = from mapped to org (going outside the airhelper to pyair)
        # in = from org to mapped (going inside from pyair to airhelper)
        self.options_map = {'out': {'requirement': {}}, 'in': {}}
        self.values_map = {'out': {}, 'in': {}}

        # Generate options dict map
        for line in open(options_map_file):
            csv = line.split(csv_indicator)
            mapped = csv[0]
            org = csv[1]
            valreq = csv[2]  # value type requirement, empty = string
            # mapped;org;comment
            self.options_map['out'][mapped] = org
            # it's only for out
            self.options_map['out']['requirement'][mapped] = valreq
            self.options_map['in'][org] = mapped

        # Generate values dict map for each map in values.map
        for line in open(values_map_file):
            csv = line.split(csv_indicator)

            command = csv[0]
            self.values_map['out'][command] = {}
            self.values_map['in'][command] = {}

            for index in range(1, len(csv)):
                if index % 2 == 0:
                    continue

                # mapped command;my;org;my2;org2
                mapped = csv[index].rstrip('\n')
                try:
                    org = csv[index+1].rstrip('\n')
                except IndexError:
                    pass

                self.values_map['out'][command][mapped] = org
                self.values_map['in'][command][org] = mapped

    # Create CoAP connection to purifier
    # Sometimes sending requests gets buggy
    # and connection needs to be recreated
    # That's why set() is returning number of tries
    def connect(self):
        self.acli = CoAPAirClient(self.host)

    # mapped here does not mean the same as csv
    # mapped is according to {direction}
    def map_opt(self, direction, opt):
        try:
            return self.options_map[direction][opt]
        except KeyError:
            return opt

    def map_opts(self, direction, opts):
        mapped_opts = {}
        for option in opts:
            mapped_opts[self.map_opt(direction, option)] = opts[option]
        return mapped_opts

    def map_val(self, direction, option, value):
        try:
            return self.values_map[direction][option][value]
        except KeyError:
            return value

    # Some values needs to be string/int/bool
    #  it's air purifier requirement..
    def check_value(self, option, value):
        requirement = self.options_map['out']['requirement'][option]
        if requirement == int_requirement:
            return int(value)
        elif requirement == bool_requirement:
            return bool(int(value))
        else:
            return str(value)

    def mapoptions(self, direction, options):
        mapped_opts = {}
        for option in options:
            mapped_option = self.map_opt(direction, option)
            mapped_value = self.map_val(direction, option, options[option])

            if direction == 'out':
                # inside this script we operate on custom options ffs
                #  mapped in this context means original ones due to
                #  direction equal to 'out' (from script to pyair)
                mapped_value = self.check_value(option, mapped_value)

            mapped_opts[mapped_option] = mapped_value
        return mapped_opts

    # get status from air purifier
    #  return dictionary of every option value
    #  or one's specified in list
    def get(self, values=[]):
        self.connect()
        status = self.mapoptions('in', self.acli.get_status())

        if len(values) == 0:
            return status

        return_status = {}

        for value in values:
            try:
                return_status[value] = status[value]
            except KeyError:
                return_status[value] = missing_key

        return return_status

    # Useful helper because sometimes sending
    # data through CoAP won't work and recreating
    # client object is only solution
    def set_values(self, values={}):
        self.connect()
        result = self.acli.set_values(values)
        del self.acli
        return result  # True/False (if setting data was successful)

    def set(self, values={}):
        correct_values = self.mapoptions('out', values)

        # Try settings at least 5 times
        iteration = 1
        while not self.set_values(correct_values):
            iteration += 1
            if iteration == 5:
                break

        return iteration  # return number of tries
