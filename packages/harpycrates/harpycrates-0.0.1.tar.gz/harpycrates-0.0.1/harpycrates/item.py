from .object_template import object_template

class item(object_template):
    # A class for generating typed, immutable, data structures

    __attributes__ = None
    __data__ = None
    __parent__ = None
    __real_class__ = None

    def __attach_attribute__(self, attr):
        # Add a variable to the item
        if len(attr) >= 2:
            var_name = attr[0]
            var_type = attr[1] if type(attr[1]) != list else attr[1][0]
            
            if type(var_name) == str and type(var_type) == type:
                var_default_value = None
                if type(attr[1]) == list and len(attr[1]) >= 2:
                    value = attr[1][1]
                    
                    if type(value) == var_type or value == None:
                        var_default_value = value
                    else:
                        raise AttributeError(attr[1][1], "is not of type", var_type)
                else:
                    if var_type == int or var_type == float:
                        var_default_value = var_type(0)
                    elif var_type == str:
                        var_default_value = ""
                    elif var_type == dict:
                        var_default_value = {}
                    else:
                        var_default_value = None

            #print(attr)
            var_default_data_index = None
            object.__getattribute__(self, "__attributes__")[var_name] = [var_type, var_default_value, var_default_data_index]
            return True

    def __call__(self):
        pass

    def __contains__(self, key):
        return key in object.__getattribute__(self, "__attributes__")

    def __getattribute__(self, key):
        attrs = object.__getattribute__(self, "__attributes__")
        rl_cls = object.__getattribute__(self, "__real_class__")
        
        if key == "keys":
            return list(object.__getattribute__(self, "__attributes__").keys())

        if key in attrs:
            return object.__getattribute__(self, "__data__")[attrs[key][2]]

        if key in dir(item) and callable(object.__getattribute__(self, key)):
             return object.__getattribute__(self, key)

        print("Attribute", key, "is not accessible.")
        exit(-1)

    def __getitem__(self, key):
        if self.__contains__(key):
            return self.__getattribute__(key)

        print(key, "does not exist")
        exit(-1)

    def __str__(self):
        attributes_string = [
            str(key) + ": " + str(self[key])
            for key in self.keys
        ]

        return "\n".join(attributes_string)

    def __instantiate__(self, struct, *args, **kwargs):
        # Create new instance and setup basic data structures
        
        if not struct:
            struct = self.__structure__()

        for key in struct:
            object.__getattribute__(self, "__attach_attribute__")([key, struct[key]])

        object.__setattr__(self, "__data__", [])        
        self.__setup_data__(self, *args, **kwargs)
        return self

    def __new__(cls, *args, **kwargs):
        struct = None
        if len(args) > 0:
            if type(args[0]) == dict:
                struct = args[0]

        parent = super(item, cls)
        self = parent.__new__(cls)
        object.__setattr__(self, "__real_class__", cls)
        object.__setattr__(self, "__parent__", parent)
        object.__setattr__(self, "__attributes__", {})

        return self.__instantiate__(struct, **kwargs)

    def __setattr__(self, key, value):
        attrs = object.__getattribute__(self, "__attributes__")
        if key in attrs:
            var_type = attrs[key][0]
            if var_type == bool and type(value) == str:
                if value and value.lower() == "true":
                    value = True
                else:
                    value = False

            if type(value) != var_type and value != None:
                print("type mismatch on", key)
                exit(-1)

            object.__getattribute__(self, "__data__")[attrs[key][2]] = value

    def __setitem__(self, key, value):
        if self.__contains__(key):
            self.__setattr__(key, value)
            return True

        print(key, "does not exist and can't be set")
        exit(-1)

    def __setup_data__(self, cls, **args):
        # Take arguments to set attributes so long as they are part of the 
        # existing structure.

        attrs = object.__getattribute__(self, "__attributes__")
        data = object.__getattribute__(self, "__data__")

        index = 0
        for var in attrs:
            variable_attrs = attrs[var]
            variable_attrs[2] = index
            value = variable_attrs[1] # default value
            
            if var in args:
                if type(args[var]) != variable_attrs[0]:
                    print(var, "must be of type", variable_attrs[0])
                    exit(-1)

                value = args[var]

            data.append(value)
            index += 1


        
    # Overwrite
    def __structure__(self):
        return {}
