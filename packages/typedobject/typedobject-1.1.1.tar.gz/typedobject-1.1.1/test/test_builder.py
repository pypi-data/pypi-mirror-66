import pytest
from typedobject import field, FrozenInstanceError, typedobject

def test_frozen():
    @typedobject.frozen
    class X:
        a: int
        b: int

    x = X(a=1, b=2)
    assert x.a == 1
    assert x.b == 2

    with pytest.raises(FrozenInstanceError):
        x.a = 3

    assert x.a == 1

def test_no_init():
    @typedobject.no_init
    class X:
        a: int
        b: int = 1

    x = X()
    assert not hasattr(x, 'a')
    assert x.b == 1

def test_equality():
    @typedobject
    class X:
        a: int = field(compare=False)
        b: int

    assert X(1, 2) == X(1, 2)
    assert X(1, 2) == X(3, 2)
    assert X(1, 2) != X(1, 3)

    with pytest.raises(TypeError):
        assert X(1, 1) < X(1, 2)

def test_no_eq():
    @typedobject.no_eq
    class X:
        a: int

    assert X(1) != X(1)

    x = X(2)
    assert x == x

def test_order():
    @typedobject.ordered
    class X:
        a: int = field(compare=False)
        b: int

    assert X(1, 1) < X(1, 2)
    assert X(3, 1) < X(1, 2)

def test_no_repr():
    @typedobject.no_repr
    class X:
        a: int

    assert repr(X(1))[0] == '<'
