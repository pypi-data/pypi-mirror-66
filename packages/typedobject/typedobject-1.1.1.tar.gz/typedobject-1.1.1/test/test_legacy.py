import pytest
from typedobject import TypedObject

def _test_legacy_slotted(x):
    assert not hasattr(x, '__dict__')

    with pytest.raises(AttributeError):
        x.non_existent = 1

def test_legacy_empty():
    class X(TypedObject):
        pass

    x = X()
    _test_legacy_slotted(x)

def test_legacy_one_field():
    class X(TypedObject):
        a: int

    with pytest.raises(TypeError):
        x = X()

    x = X(1)
    _test_legacy_slotted(x)
    assert x.a == 1

    x = X(a=2)
    _test_legacy_slotted(x)
    assert x.a == 2

    x.a = 4
    assert x.a == 4

def test_legacy_one_field_with_default():
    class X(TypedObject):
        a: int = 10

    x = X()
    _test_legacy_slotted(x)
    assert x.a == 10

    x = X(1)
    _test_legacy_slotted(x)
    assert x.a == 1

    x = X(a=2)
    _test_legacy_slotted(x)
    assert x.a == 2

    x.a = 4
    assert x.a == 4

def test_legacy_two_fields():
    class X(TypedObject):
        a: int
        b: int

    with pytest.raises(TypeError):
        x = X()
    with pytest.raises(TypeError):
        x = X(1)

    x = X(1, 2)
    _test_legacy_slotted(x)
    assert x.a == 1
    assert x.b == 2

    x = X(3, b=4)
    _test_legacy_slotted(x)
    assert x.a == 3
    assert x.b == 4

    x = X(b=5, a=6)
    _test_legacy_slotted(x)
    assert x.a == 6
    assert x.b == 5

def test_legacy_trailing_defaults():
    class X(TypedObject):
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

def test_legacy_leading_defaults():
    class X(TypedObject):
        a: int = 51
        b: int

    with pytest.raises(TypeError):
        x = X()

    with pytest.raises(TypeError):
        x = X(1, 2)

    x = X(a=3, b=4)
    assert x.a == 3
    assert x.b == 4

    x = X(b=5)
    assert x.a == 51
    assert x.b == 5

def test_legacy_inheritance():
    class X(TypedObject):
        a: int
        b: int

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


def test_legacy_no_dunder():
    with pytest.raises(TypeError):
        # pylint: disable=unused-variable
        class X(TypedObject):
            __hello__: int

def test_legacy_superprivate():
    class X(TypedObject):
        __hello: int

        def foo(self):
            return self.__hello

    x = X(1)
    assert x.foo() == 1

class X(TypedObject):
    a: int = 42
    b: int

    def __init__(self, b):
        assert self.a == 42
        self.b = b

def test_legacy_custom_init():
    x = X(1)
    assert x.a == 42
    assert x.b == 1

class Y(X):
    c: int

def test_legacy_derived_init():
    with pytest.raises(TypeError):
        Y(1)

    x = Y(b=3, c=4)
    assert x.a == 42
    assert x.b == 3
    assert x.c == 4

def test_legacy_readme():
    # pylint: disable=unused-variable

    from typedobject import TypedObject

    class Point(TypedObject):
        x: int
        y: int

    pt1 = Point(10, 20)
    pt2 = Point(x=10, y=20)
    assert pt1 == pt2

    class Rectangle(TypedObject):
        pt1: Point
        pt2: Point

        def __init__(self, x1, y1, x2, y2):
            self.pt1 = Point(x1, y1)
            self.pt2 = Point(x2, y2)

        def area(self):
            return (self.pt2.x - self.pt1.x) * (self.pt2.y - self.pt1.y)

    rect = Rectangle(1, 1, 3, 3)
    assert rect.area() == 4

    assert isinstance(rect, Rectangle)
    assert not isinstance(rect, Point)

    class RoundedRect(Rectangle):
        corner_radius: int

    rr = RoundedRect(Point(1, 1), Point(3, 3), 1)

    with pytest.raises(AttributeError):
        rect.width = 2

    with pytest.raises(TypeError):
        class RectangleWithAPoint(Rectangle, Point):
            pass
