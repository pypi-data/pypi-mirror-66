import pytest
from typedobject import typedobject

@typedobject
class X:
    a: int = 42
    b: int

    def __init__(self, b):
        assert self.a == 42
        self.b = b

def test_custom_init():
    x = X(1)
    assert x.a == 42
    assert x.b == 1

@typedobject
class Y(X):
    c: int

def test_derived_init():
    with pytest.raises(TypeError):
        Y(1)

    x = Y(b=3, c=4)
    assert x.a == 42
    assert x.b == 3
    assert x.c == 4
