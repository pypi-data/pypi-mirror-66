from typing import Any, Callable, Tuple, Mapping
from ._meta import TypedObjectMeta

class TypedObject(metaclass=TypedObjectMeta):
    __fields__: Tuple[str, ...]
    __field_defaults__: Mapping[str, Any]
    __init_fields__: Callable[..., None]

    # pylint: disable=no-method-argument
    def __new__(*args, **kw):
        cls, *args = args
        self = object.__new__(cls)
        if cls.__init__ is not cls.__init_fields__:
            for k, v in cls.__field_defaults__.items():
                setattr(self, k, v)
        return self

    def __repr__(self):
        cls = type(self)
        args = ', '.join(f'{field}={getattr(self, field)!r}' for field in cls.__fields__)
        return f'{cls.__name__}({args})'

    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return all(getattr(self, k) == getattr(other, k) for k in self.__fields__)
