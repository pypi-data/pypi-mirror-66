import pytest
from typedobject import typedobject


def test_no_dunder():
    with pytest.raises(TypeError):
        @typedobject
        class _X:
            __hello__: int

def test_superprivate():
    @typedobject
    class X:
        __hello: int

        def foo(self):
            return self.__hello

    x = X(1)
    assert x.foo() == 1
