from .config import config_instance
from .item import item
from .object_template import object_template
from . import oblog

class thing_method:
    def __contains__(self, key):
        return key in self.__dict__

    def __getitem__(self, key):
        if key in self.subroutines:
            return self.subroutines[key]

        return self.__dict__[key]

    def __init__(self, parent):
        self.parent = parent
        self.subroutines = {}
        self.arguments = {}

    def public(self, func):
        # Add a function to the methods list

        self.arguments[func.__name__] = list(
            func.__code__.co_varnames[:func.__code__.co_argcount]
        )

        def wrapper(*args, **kwargs):
            return func(self.parent, *args, **kwargs)

        self.__dict__[func.__name__] = wrapper

class thing(object_template):
    __args__ = None
    __dict__ = None
    __methods_obj__ = None
    __item__ = None

    def __getattribute__(self, key):
        
        if key == "__classname__":
            return object.__getattribute__(self, "__class__").__name__

        if key in object.__getattribute__(self, "__item__"):
            return object.__getattribute__(self, "__item__")[key]

        if key in object.__getattribute__(self, "__methods_obj__"):
            return object.__getattribute__(self, "__methods_obj__")[key]

    def __new__(cls, *args, **kwargs):
        parent = super(thing, cls)
        self = parent.__new__(cls)

        struct = object.__getattribute__(self, "__structure__")()
        if struct:
            object.__setattr__(self, "__item__", item(struct))
        object.__setattr__(self, "__methods_obj__", thing_method(self))
        
        object.__getattribute__(self, "__parse_methods__")(*args, **kwargs)
        return self

    def __parse_methods__(self, *args, **kwargs):
        methods = object.__getattribute__(self, "__methods__")
        methods(object.__getattribute__(self, "__methods_obj__"))
        methods_obj = object.__getattribute__(self, "__methods_obj__")
        
        constructor_name = "__%s__" % self.__classname__
        if methods_obj.__contains__(constructor_name):
            constructor = object.__getattribute__(self, "__methods_obj__")[constructor_name]
            constructor(*args, **kwargs)

    def __setattr__(self, key, value):
        if key in object.__getattribute__(self, "__item__"):
            object.__getattribute__(self, "__item__")[key] = value

        #object.__getattribute__(self, "__oblog__")()

    def __methods__(self, methods):
        pass

    def __structure__(self):
        pass