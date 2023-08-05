import pytest
from typedobject import typedobject

def _test_slotted(x):
    assert not hasattr(x, '__dict__')

    with pytest.raises(AttributeError):
        x.non_existent = 1

def test_empty():
    @typedobject
    class X:
        pass

    x = X()
    _test_slotted(x)

    assert repr(x) == 'X()'

def test_one_field():
    @typedobject
    class X:
        a: int

    with pytest.raises(TypeError):
        x = X()

    x = X(1)
    _test_slotted(x)
    assert x.a == 1

    x = X(a=2)
    _test_slotted(x)
    assert x.a == 2

    x.a = 4
    assert x.a == 4

    assert repr(x) == 'X(a=4)'

def test_one_field_with_default():
    @typedobject
    class X:
        a: int = 10

    x = X()
    _test_slotted(x)
    assert x.a == 10

    x = X(1)
    _test_slotted(x)
    assert x.a == 1

    x = X(a=2)
    _test_slotted(x)
    assert x.a == 2

    x.a = 4
    assert x.a == 4

def test_two_fields():
    @typedobject
    class X:
        a: int
        b: int

    with pytest.raises(TypeError):
        x = X()
    with pytest.raises(TypeError):
        x = X(1)

    x = X(1, 2)
    _test_slotted(x)
    assert x.a == 1
    assert x.b == 2

    x = X(3, b=4)
    _test_slotted(x)
    assert x.a == 3
    assert x.b == 4

    x = X(b=5, a=6)
    _test_slotted(x)
    assert x.a == 6
    assert x.b == 5

def test_trailing_defaults():
    @typedobject
    class X:
        a: int
        b: int = 50

    with pytest.raises(TypeError):
        x = X()

    x = X(1)
    assert x.a == 1
    assert x.b == 50

    x = X(2, 3)
    assert x.a == 2
    assert x.b == 3

    x = X(a=4, b=5)
    assert x.a == 4
    assert x.b == 5

def test_inheritance():
    @typedobject
    class X:
        a: int
        b: int

    @typedobject
    class Y(X):
        c: int

    y = Y(1, 2, 3)

    # pylint: disable=no-member
    assert y.a == 1
    assert y.b == 2
    assert y.c == 3

    y = Y(a=1, b=2, c=3)
    assert y.a == 1
    assert y.b == 2
    assert y.c == 3

    assert isinstance(y, Y)
    assert isinstance(y, X)
