from components.air_pyrifier_server import Air_pyrifier_server
from components.air_pyrifier_client import Air_pyrifier_client
from components.air_pyrifier_local import Air_pyrifier_local
from helpers.config import Config


class Run_util(Config):
    @staticmethod
    def get_server_fn(name):
        SERVER_BASED_ACTIONS = {
            'listen': Run_util.server_listen,
            'get': Run_util.client_get,
            'status': Run_util.client_status,
            'set': Run_util.client_set
        }

        return SERVER_BASED_ACTIONS[name]

    @staticmethod
    def get_local_fn(name):
        LOCAL_BASED_ACTIONS = {
            'get': Run_util.local_get,
            'status': Run_util.local_status,
            'set': Run_util.local_set
        }

        return LOCAL_BASED_ACTIONS[name]

    @staticmethod
    def server_listen(options):
        return Air_pyrifier_server().listen()

    @staticmethod
    def client_get(options):
        return Air_pyrifier_client().get(options)

    @staticmethod
    def client_status(options):
        return Air_pyrifier_client().status()

    @staticmethod
    def client_set(options):
        return Air_pyrifier_client().set(options)

    @staticmethod
    def local_get(host, options):
        return Air_pyrifier_local(host).get(options)

    @staticmethod
    def local_status(host, options):
        return Air_pyrifier_local(host).status()

    @staticmethod
    def local_set(host, options):
        return Air_pyrifier_local(host).set(options)

    @staticmethod
    def dispatcher(name, args):
        if name == 'local':
            return Run_util.local_dispatcher(args)

        return Run_util.get_server_fn(name)(args)

    @staticmethod
    def local_dispatcher(args):
        host = args[0]
        action = args[1]
        options = args[2:] if len(args) >= 3 else []

        return Run_util.get_local_fn(action)(host, options)