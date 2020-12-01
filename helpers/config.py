import os
from helpers.file_util import File_util


class Config(File_util):
    CONFIG_FILE = 'config.json'

    KEY_SECRET_KEY = 'secret_key'
    KEY_PURIFIER_ADDRESS = 'purifier_address'

    KEY_SERVER_LISTEN_ADDRESS = 'server_listen_address'
    KEY_SERVER_LISTEN_PORT = 'server_listen_port'
    KEY_SERVER_WS_ADDRESS = 'server_ws_address'

    @staticmethod
    def get_secret():
        return Config._get_config_option(Config.KEY_SECRET_KEY)

    @staticmethod
    def get_purifier_address():
        return Config._get_config_option(Config.KEY_PURIFIER_ADDRESS)

    @staticmethod
    def get_server_listen_address():
        return Config._get_config_option(Config.KEY_SERVER_LISTEN_ADDRESS)

    @staticmethod
    def get_server_listen_port():
        return Config._get_config_option(Config.KEY_SERVER_LISTEN_PORT)

    @staticmethod
    def get_server_ws_address():
        return Config._get_config_option(Config.KEY_SERVER_WS_ADDRESS)

    @staticmethod
    def _get_config_option(key):
        config = Config.get_config()

        if config[key] is None:
            raise Exception(f'Couldn\'t find {key} in {Config.CONFIG_FILE}')

        return config[key]

    @staticmethod
    def get_config():
        return Config.get_json_file(Config.CONFIG_FILE)
