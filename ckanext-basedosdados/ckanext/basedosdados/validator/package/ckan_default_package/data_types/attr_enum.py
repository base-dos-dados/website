from enum import EnumMeta, Enum

class _EnumMeta(EnumMeta):
    def __new__(meta, name, bases, namespace, **kw):
        members = namespace._member_names
        namespace._member_names = []
        namespace._last_values = []
        for k in members:
            assert isinstance(namespace[k], dict)
            value = namespace.pop(k)
            namespace[k] = (k, value)
        return super().__new__(_EnumMeta, name, bases, namespace, **kw)

class AttrEnum(str, Enum, metaclass=_EnumMeta):
    ''' An enum class that does two things:
        * Infers the enum name from the variable name.
        * Saves your argument on a `attrs` property

    >>> class Animal(AttrEnum):
    >>>    DOG = dict(size=10, weight=20)
    >>>    CAT = dict(size=5, weight=10)

    >>> Animal.DOG.attr['size']
    20
    >>> Animal('CAT').attr['weight']
    10
    '''

    def __new__(cls, value, attr):
        obj = str.__new__(cls, value)
        obj._name_ = value
        obj._value_ = value
        obj.attr = attr
        return obj

    @classmethod
    def get_all_enum_attr(cls, attr):
        '''
        >>> class Animal(AttrEnum):
        >>>    DOG = dict(size=10, weight=20)
        >>>    CAT = dict(size=5, weight=10)

        >>> Animal.get_all_enum_attr('size')
        {'DOG': 10, 'CAT': 5}
        '''
        return {name: obj.attr.get(attr) for name, obj in cls.__members__.items()}
