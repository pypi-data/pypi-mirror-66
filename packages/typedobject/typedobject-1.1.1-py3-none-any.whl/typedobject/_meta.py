import ast
import inspect

class TypedObjectMeta(type):
    def __new__(metacls, name, bases, ns):
        annots = ns.get('__annotations__', {})
        annots.pop('__fields__', None)
        annots.pop('__field_defaults__', None)
        annots.pop('__init_fields__', None)

        for k in annots:
            if k.startswith('__'):
                raise TypeError(f'{name}.{k}: field names must not start with a double underscore')

        slots = tuple(annots)
        defaults = { k: ns.pop(k) for k in slots if k in ns }
        ns['__defaults__'] = defaults
        ns['__slots__'] = slots
        cls = type.__new__(metacls, name, bases, ns)

        fields = []
        field_defaults = {}
        for base in reversed(inspect.getmro(cls)):
            if isinstance(base, metacls):
                fields.extend(getattr(base, '__annotations__', ()))
                field_defaults.update(getattr(base, '__defaults__', {}))

        cls.__fields__ = fields
        cls.__field_defaults__ = field_defaults

        fr = inspect.currentframe().f_back
        filename = fr.f_code.co_filename
        lineno = fr.f_lineno
        del fr
        cls.__init_fields__ = _compile_init(filename, lineno, fields, field_defaults)

        if '__init__' not in ns:
            cls.__init__ = cls.__init_fields__

        return cls

def _compile_init(filename, lineno, fields, field_defaults):
    coords = { 'lineno': lineno, 'col_offset': 1 }

    args = [ast.arg(arg='self', **coords)]
    defaults = []

    i = 0
    for name in fields:
        if name in field_defaults:
            args.append(ast.arg(arg=name, **coords))
            defaults.append(field_defaults[name])
        elif defaults:
            break
        else:
            args.append(ast.arg(arg=name, **coords))
        i += 1

    kwonlyargs = []
    kwdefaults = {}
    for name in fields[i:]:
        kwonlyargs.append(ast.arg(arg=name, **coords))
        if name in field_defaults:
            kwdefaults[name] = field_defaults[name]

    body = []
    for name in fields:
        body.append(ast.Assign(
            targets=[ast.Attribute(
                value=ast.Name('self', ctx=ast.Load(), **coords),
                attr=name,
                ctx=ast.Store(),
                **coords)],
            value=ast.Name(name, ast.Load(), **coords),
            **coords))

    if not body:
        body.append(ast.Pass(**coords))

    args = ast.arguments(
        posonlyargs=[],
        args=args,
        kwonlyargs=kwonlyargs,
        kw_defaults=[None] * len(kwonlyargs),
        defaults=[])

    fndef = ast.FunctionDef(name='__init_fields__', args=args, body=body, decorator_list=[], **coords)
    mod = ast.Module([fndef], type_ignores=[])

    code = compile(mod, filename, 'exec')

    d = {}
    exec(code, d)

    r = d['__init_fields__']
    r.__defaults__ = tuple(defaults)
    r.__kwdefaults__ = kwdefaults
    return r
