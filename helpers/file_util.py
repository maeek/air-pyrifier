import os
import json


class File_util:
    @staticmethod
    def get_json_file(file_path):
        return json.load(File_util.get_file(file_path))

    @staticmethod
    def get_file(file_path):
        if File_util._check_file(file_path):
            try:
                file = open(file_path)

                return file

            except:
                return {}

        else:
            raise Exception(f'File not found, path: {file_path}')

    @staticmethod
    def _check_file(file_path):
        return os.path.exists(file_path)
