from . import oblog

class object_template(object):
    __number__ = 0

    def __new__(cls):
        cls.__number__ += 1
        return super(object_template, cls).__new__(cls)

    def __oblog__(self):
        oblog.log(self)