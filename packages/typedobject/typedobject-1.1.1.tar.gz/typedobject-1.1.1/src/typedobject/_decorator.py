import ast
from dataclasses import Field, field, MISSING, FrozenInstanceError
import inspect

class TypedObjectMixin:
    # pylint: disable=no-method-argument
    def __new__(*args, **kw):
        cls, *args = args
        self = object.__new__(cls)

        if getattr(cls, '__init__', None) is not cls.__init_fields__:
            setattr = object.__setattr__
            for name, spec in cls.__fields__:
                if spec.default is not MISSING:
                    setattr(self, name, spec.default)
                elif spec.default_factory is not MISSING:
                    setattr(self, name, spec.default_factory())

        return self

    def __init_fields__(*args, **kw):
        self, *args = args
        setattr = object.__setattr__
        it = iter(self.__fields__)
        src = None

        if args and isinstance(args[0], type(self)):
            src, *args = args

        for arg in args:
            while True:
                try:
                    name, field = next(it)
                except StopIteration:
                    raise TypeError('too many positional arguments') from None
                if field.init:
                    setattr(self, name, arg)
                    break

        for name, field in it:
            if not field.init:
                continue

            if name in kw:
                setattr(self, name, kw.pop(name))
            elif src is not None:
                setattr(self, name, getattr(src, name))
            elif field.default is not MISSING:
                setattr(self, name, field.default)
            elif field.default_factory is not MISSING:
                setattr(self, name, field.default_factory())
            else:
                raise TypeError(f'{name}: required argument not provided')

        if kw:
            k, _v = kw.popitem()
            raise TypeError(f'{k}: no such argument')

    def __getstate__(self):
        return tuple((name, getattr(self, name)) for name, _ in self.__fields__)

    def __setstate__(self, state):
        setattr = object.__setattr__
        for name, value in state:
            setattr(self, name, value)

    def __repr__(self):
        params = [f'{name}={getattr(self, name)!r}' for name, spec in self.__fields__ if spec.repr]
        return f'{type(self).__name__}({", ".join(params)})'

    def __setattr__(self, name, value):
        raise FrozenInstanceError(name)

    def __delattr__(self, name):
        raise FrozenInstanceError(name)

    def __hash__(self):
        return hash(tuple(getattr(self, name) for name, field in self.__fields__ if field.hash))

    def __eq__(self, other):
        if self.__fields__ is not getattr(other, '__fields__', ()):
            return NotImplemented
        return all(getattr(self, name) == getattr(other, name) for name, field in self.__fields__ if field.compare)

    def __ne__(self, other):
        eq = self == other
        if eq is NotImplemented:
            return NotImplemented
        return not eq

    def __lt__(self, other):
        if self.__fields__ is not getattr(other, '__fields__', ()):
            return NotImplemented
        return (tuple(getattr(self, name) for name, field in self.__fields__ if field.compare)
            < tuple(getattr(other, name) for name, field in self.__fields__ if field.compare))

    def __gt__(self, other):
        return other < self

    def __le__(self, other):
        n = other < self
        if n is NotImplemented:
            return NotImplemented
        return not n

    def __ge__(self, other):
        n = self < other
        if n is NotImplemented:
            return NotImplemented
        return not n

class TypedObjectBuilder:
    def __init__(self, *, init, repr, eq, order, frozen):
        self._init = init
        self._repr = repr
        self._eq = eq
        self._order = order
        self._frozen = frozen

    def __call__(self, *args, init=MISSING, repr=MISSING, eq=MISSING, order=MISSING, frozen=MISSING):
        if not args:
            if init is MISSING:
                init = self._init
            if repr is MISSING:
                repr = self._repr
            if eq is MISSING:
                eq = self._eq
            if order is MISSING:
                order = self._order
            if frozen is MISSING:
                frozen = self._frozen
            return TypedObjectBuilder(init=init, repr=repr, eq=eq, order=order, frozen=frozen)
        elif len(args) == 1:
            return self._build_from_template(args[0])
        else:
            return self._build(*args)

    def _build_from_template(self, template):
        metacls = type(template)

        ns = dict(template.__dict__)
        annots = ns.get('__annotations__', {})
        defaults = { k: ns.pop(k) for k in annots if k in ns }

        fields = {}
        for k in annots:
            if k.startswith('__'):
                raise TypeError(f'{template.__name__}.{k}: field names must not start with a double underscore')

            if k not in defaults:
                fields[k] = field()
            else:
                v = defaults[k]
                if isinstance(v, Field):
                    fields[k] = v
                else:
                    fields[k] = field(default=v)

        return self._build(template.__name__, fields, template.__bases__, ns, metacls)

    def _build(self, clsname, fields, bases=(), ns=(), metacls=type):
        if not issubclass(metacls, type):
            raise TypeError('typedobject doesn\'t work with classes that are not instances of type')

        ns = dict(ns)
        ns.pop('__dict__', None)
        ns.pop('__weakref__', None)

        for base in bases:
            for name, _field in getattr(base, '__fields__', ()):
                if name in fields:
                    raise TypeError(f'{name}: already defined in {base.__name__}')

        ns['__slots__'] = tuple(fields)
        ns['__new__'] = TypedObjectMixin.__new__
        ns['__init_fields__'] = TypedObjectMixin.__init_fields__
        if self._init and '__init__' not in ns:
            ns['__init__'] = TypedObjectMixin.__init_fields__
        ns['__getstate__'] = TypedObjectMixin.__getstate__
        ns['__setstate__'] = TypedObjectMixin.__setstate__
        if self._repr:
            ns['__repr__'] = TypedObjectMixin.__repr__
        if self._frozen:
            ns['__setattr__'] = TypedObjectMixin.__setattr__
            ns['__delattr__'] = TypedObjectMixin.__delattr__
        if self._eq:
            if '__hash__' not in ns:
                ns['__hash__'] = TypedObjectMixin.__hash__
            if '__eq__' not in ns:
                ns['__eq__'] = TypedObjectMixin.__eq__
            ns['__ne__'] = TypedObjectMixin.__ne__
        if self._order:
            if '__lt__' not in ns:
                ns['__lt__'] = TypedObjectMixin.__lt__
            ns['__gt__'] = TypedObjectMixin.__gt__
            ns['__le__'] = TypedObjectMixin.__le__
            ns['__ge__'] = TypedObjectMixin.__ge__
        cls = metacls(clsname, bases, ns)

        all_fields = {}
        for base in reversed(inspect.getmro(cls)):
            all_fields.update(getattr(base, '__fields__', ()))

        for name in ns:
            fld = all_fields.get(name)
            if fld is not None:
                all_fields[name] = field(init=False, compare=fld.compare, repr=fld.repr)

        all_fields.update(fields)
        cls.__fields__ = tuple(all_fields.items())
        return cls

    @property
    def no_init(self):
        return TypedObjectBuilder(init=False, repr=self._repr, eq=self._eq, order=self._order, frozen=self._frozen)

    @property
    def no_repr(self):
        return TypedObjectBuilder(init=self._init, repr=False, eq=self._eq, order=self._order, frozen=self._frozen)

    @property
    def no_eq(self):
        return TypedObjectBuilder(init=self._init, repr=self._repr, eq=False, order=self._order, frozen=self._frozen)

    @property
    def frozen(self):
        return TypedObjectBuilder(init=self._init, repr=self._repr, eq=self._eq, order=self._order, frozen=True)

    @property
    def ordered(self):
        return TypedObjectBuilder(init=self._init, repr=self._repr, eq=self._eq, order=True, frozen=self._frozen)

typedobject = TypedObjectBuilder(init=True, repr=True, eq=True, order=False, frozen=False)
