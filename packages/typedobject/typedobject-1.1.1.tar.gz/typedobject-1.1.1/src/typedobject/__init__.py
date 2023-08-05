from ._object import TypedObject
from ._decorator import field, FrozenInstanceError, typedobject

def assign(dest, src):
    for name, _fld in dest.__fields__:
        setattr(dest, name, getattr(src, name))

def fresh(default_factory):
    return field(default_factory=default_factory)

def visit(visitor, obj, *args, **kw):
    from inspect import getmro

    for tp in getmro(type(obj)):
        m = f'visit_{tp.__name__}'
        vm = getattr(visitor, m, None)
        if vm is not None:
            return vm(obj, *args, **kw)

    if hasattr(obj, '__fields__'):
        for name, _field in obj.__fields__:
            v = getattr(obj, name)
            visit(visitor, v, *args, **kw)
