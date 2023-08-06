import os
from .item import item

class configuration(item):
    def __init__(self):
        for key in self.keys:
            if key != "prefix":
                actual_key = self.prefix + key
                value = os.environ.get(actual_key)
                if value:
                    self[key] = value

    def __structure__(cls):
        return {
            'oblog_directory': [str, "/tmp/oblog"],
            'oblog_on': [bool, False],
            'prefix': [str, "harpycrates_"]
        }

config_instance = configuration()
