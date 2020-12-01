from helpers.file_util import File_util
import os


class Maps_util(File_util):
    MAP_CSV_DELIMITER = ';'

    RESOURCES_PATH = 'resources'

    OPTIONS_MAP_PATH = 'options.map'
    OPTIONS_MAP_DICT = {'out': {'requirement': {}}, 'in': {}}

    VALUES_MAP_PATH = 'values.map'
    VALUES_MAP_DICT = {'out': {}, 'in': {}}

    @staticmethod
    def get_options():
        options_path = os.path.join(Maps_util.RESOURCES_PATH, Maps_util.OPTIONS_MAP_PATH)

        options_file = Maps_util.get_file(options_path)

        options_map = dict(Maps_util.OPTIONS_MAP_DICT)

        for line in options_file:
            csv = line.split(Maps_util.MAP_CSV_DELIMITER)

            mapped = csv[0]
            org = csv[1]
            valreq = csv[2]  # value type requirement, empty = string

            # mapped;org;comment
            # it's only for out
            options_map['out'][mapped] = org
            options_map['out']['requirement'][mapped] = valreq
            options_map['in'][org] = mapped

        return options_map

    @staticmethod
    def get_values():
        values_path = os.path.join(Maps_util.RESOURCES_PATH, Maps_util.VALUES_MAP_PATH)

        values_file = Maps_util.get_file(values_path)

        values_map = dict(Maps_util.VALUES_MAP_DICT)

        for line in values_file:
            csv = line.split(Maps_util.MAP_CSV_DELIMITER)

            command = csv[0]
            values_map['out'][command] = {}
            values_map['in'][command] = {}

            for index in range(1, len(csv)):
                if index % 2 == 0:
                    continue

                # mapped command;my;org;my2;org2
                mapped = csv[index].rstrip('\n')
                try:
                    org = csv[index+1].rstrip('\n')
                except IndexError:
                    pass

                values_map['out'][command][mapped] = org
                values_map['in'][command][org] = mapped

        return values_map
