from spira.core.param.restrictions import RestrictNothing


__all__ = ['DataFieldDescriptor', 'FunctionField', 'DataField']


class BaseField(object):
    """
    Sets the values of the Field when initialized.
    Binds a Field object with a class parameter.

    class Via(spira.Cell):
        layer = param.LayerField()

    >>> via = Via()
    >>> via.layer
    <spira.yevon.gdsii.DataFieldDescriptor>
    >>> via.layer.default
    [SPiRA: Layer] (name '', number 0, datatype 0)
    """

    __keywords__ = ['default', 'fdef_name', 'locked', 'doc']

    def __init__(self, **kwargs):
        self.__doc__ = 'No documenation generated'
        if 'doc' in kwargs:
            self.__doc__ = kwargs['doc']
            kwargs.pop('doc')
        for k, v in kwargs.items():
            if k in self.__keywords__:
                object.__setattr__(self, k, v)

    def bind_property(self, cls, name):
        pass

    def validate_binding(self, host_cls, name):
        return True


class DataFieldDescriptor(BaseField):
    __keywords__ = ['default', 'fdef_name', 'restrictions', 'locked']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.locked = False

        if 'allow_none' in kwargs:
            self.allow_none = kwargs['allow_none']
        else:
            self.allow_none = False

        if 'restriction' in kwargs:
            self.restriction = kwargs['restriction']
        else:
            self.restriction = RestrictNothing()

        if 'fdef_name' not in kwargs:
            self.fdef_name = None

    def __field_was_stored__(self, obj):
        return (self.__name__ in obj.__store__)

    def __check_restriction__(self, obj, value):
        if (self.allow_none is True) and (value is None):
            return True
        elif self.restriction(value, obj):
            return True
        else:
            raise ValueError("Invalid parameter assignment '{}' of cell '{}' with value '{}', which is not compatible with '{}'.".format(self.name, obj.__class__.__name__, str(value), str(self.restriction)))

    def __get__(self, obj, type=None):
        """
        Called when retieving a value from an instance.
        Following from `via` in __set__, the following
        can be executed:

        Information:
        >>> via.layer
        50
        """
        if obj is None:
            return self
        if not self.__field_was_stored__(obj):
            f = self.get_param_function(obj)
            if f is None:
                if hasattr(self, 'default'):
                    value = self.default
                else:
                    value = None
            else:
                value = self.call_param_function(obj)
        else:
            value = self.get_stored_value(obj)
        if not self.restriction(value, obj):
            if value is None:
                if not self.allow_none:
                    raise ValueError("Cannot set parameter {} of {} to None.".format(self.name, obj.__class__.__name__))
            else:
                raise ValueError("Invalid parameter assignment '{}' of cell '{}' with value '{}', which is not compatible with '{}'.".format(self.name, obj.__class__.__name__, str(value), str(self.restriction)))
        # self.__check_restriction__(obj, value)
        return value

    def __set__(self, obj, value):
        """
        Store the value of the object keyword argument
        in the __store__ variable of the instance. This
        setter is calle from the FieldInitializer class.
        This is called when creating a class instance:

        self -> The Field being set.
        obj -> Class to which value are set.

        -------------------------------------------------
        class Via(spira.Cell):
            layer = param.LayerField()

        via = Via(layer=50)
        -------------------------------------------------

        Information:
        >>> via.__store__['__param_layer__']
        50
        >>> obj.__class__.__name__
        Via
        """
        if self.locked:
            raise ValueError("Cannot assign to locked parameter '{}' of '{}'".format(self.name, type(obj).__name__))
        self.__check_restriction__(obj, value)
        obj.__store__[self.__name__] = value

    def bind_property(self, cls, name):
        self.name = name
        if not hasattr(self, '__name__'):
            self.__name__ = '__param_{}__'.format(name)

    def validate_binding(self, host_cls, name):
        if self.fdef_name is None:
            self.auto_fdef_name = 'create_' + name

    def get_stored_value(self, obj):
        value = obj.__store__[self.__name__]
        return value

    def get_param_function(self, obj):
        if self.fdef_name is None:
            if hasattr(obj, self.auto_fdef_name):
                return getattr(obj, self.auto_fdef_name)
            else:
                return None
        else:
            return getattr(obj, self.fdef_name)

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f()
        obj.__store__[self.__name__] = value
        return value


class FunctionField(BaseField):
    """ Property which calls a get and set method to set the variables.
    the get and set method are specified by name, so it supports override,
    but is slower than FunctionProperty. If set method is not specified,
    then the property is considered locked and cannot be set.
    
    Examples
    --------
    """

    def __init__(self, fget, fset=None, **kwargs):
        self.fget = fget
        if fset is None:
            self.locked = True
        else:
            self.fset = fset
            self.locked = False
        BaseField.__init__(self, **kwargs)

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return self.fget(obj)

    def __set__(self, obj, value):
        if not self.locked:
            return self.fset(obj, value)
        else:
            raise ValueError('Cannot assign parameter.')


class SetFunctionField(BaseField):
    """property which calls a set method to set the variables,
    but it is stored in a known attribute, so a get method
    need not be specified. A restriction can be specified."""

    def __init__(self, internal_member_name, fset, **kwargs):
        self.fset = fset
        self.__name__ = internal_member_name
        self.name = internal_member_name
        self.locked = False
        self.allow_none = False
        if 'restriction' in kwargs:
            self.restriction = kwargs['restriction']
        else:
            self.restriction = RestrictNothing()
        super().__init__(**kwargs)

    def __get_default__(self):
        import inspect
        if inspect.isroutine(self.default):
            return self.default()
        else:
            return self.default

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        if (self.__name__ in obj.__dict__):
            return obj.__dict__[self.__name__]
        else:
            if hasattr(self, 'default'):
                d = self.__get_default__()
                return d
                # if self.preprocess is None:
                #     return d
                # else:
                #     return self.preprocess(d, obj)
            elif self.allow_none:
                return None
            else:
                raise ValueError("Attribute '%s' of '%s' is not set, and no default value is specified" (self.name, obj))

    def __set__(self, obj, value):
        if self.restriction(value, obj):
            return self.fset(obj, value)
        else:
            raise ValueError("%s does not match restriction %s in property %s" % (value, self.restriction, self.__name__))

    def bind_property(self, cls, name):
        self.name = name
        if self.__name__ is None:
            self.__name__ = '__prop_{}__'.format(name)


import sys

def is_call_internal(obj, level=1):
    """ checks if a call to a function is done from within the object
        or from outside """
    f = sys._getframe(1 + level).f_locals
    if not "self" in f:
        return False
    return (f["self"] is obj)


class ConvertField(BaseField):

    def __init__(self, parent_class, parent_property_name, convert_method):
        self.convert_method = convert_method
        self.parent_class = parent_class
        self.parent_property_name = parent_property_name
        self.locked = True
        BaseField.__init__(self)

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return self.parent_property.__get__(obj, type)

    def __set__(self, obj, value):
        if not is_call_internal(obj):
            self.convert_method(obj)
        value = self.parent_property.__set__(obj, value)
        return value

    def bind_property(self, cls, name):
        import inspect
        self.name = name
        if None == self.parent_property_name:
            self.parent_property_name = name
        # if None == self.parent_class:
        #     mro = inspect.getmro(cls)
        #     found = False
        #     for C in mro[1:]:
        #         if name in C.__store__:
        #             if isinstance(C.__store__[name][0], DefinitionProperty):
        #                 continue
        #             self.parent_class = C
        #             found = True
        #             break
        #     if not found:
        #         raise IpcorePropertyDescriptorException("DefinitionProperty '%s' of '%s' should have a matching property in a parent class." % (name, cls))
        self.parent_property = object.__getattribute__(self.parent_class, self.parent_property_name)


class DataField(DataFieldDescriptor):
    pass




